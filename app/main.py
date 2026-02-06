from fastapi import FastAPI, Query, HTTPException, Depends
from pathlib import Path
from typing import List, Dict
from fastapi.security import OAuth2PasswordRequestForm
import urllib.parse

from app.shroomloc import get_mushrooms, get_all_mushrooms, get_mushroom_details_by_name
from app.auth import verify_password, create_access_token, get_current_user
from app.db import SessionLocal, User, init_db

init_db()


app = FastAPI(
    title="ShroomLoc API",
    version="0.2.0",
    description="Mushroom location and identification API"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "mushrooms_cleaned.json"

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.username == form_data.username).first()
    db.close()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}

@app.get("/mushrooms", response_model=List[Dict])
def mushrooms(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    """
    Return a list of mushrooms filtered by environmental conditions
    at the given latitude and longitude.

    Args:
        latitude (float): Latitude of the location (-90 to 90)
        longitude (float): Longitude of the location (-180 to 180)

    Returns:
        List[Dict]: List of mushrooms with scientific name, common name,
                    edibility, and image URL.
    """
    return get_mushrooms(latitude, longitude, DATA_FILE)


@app.get("/mushrooms/all", response_model=List[Dict])
def list_all_mushrooms(current_user: User = Depends(get_current_user)) -> List[Dict]:
    """
    Return the full list of mushrooms from the dataset.

    Returns:
        List[Dict]: List of all mushrooms with their properties.
    """
    return get_all_mushrooms()

@app.get("/mushrooms/{name}", response_model=Dict)
def get_mushroom_by_name(name: str, current_user: User = Depends(get_current_user)) -> Dict:
    """
    Return details of a specific mushroom by its scientific or common name.

    Args:
        name (str): Scientific or common name of the mushroom to search for.
    returns:
        Dict: Details of the mushroom if found, otherwise an error message.
    """
    decoded_name = urllib.parse.unquote(name)
    mushroom = get_mushroom_details_by_name(decoded_name)
    if mushroom:
        return mushroom
    else:
        raise HTTPException(status_code=404, detail="Mushroom not found")

