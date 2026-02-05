from fastapi import FastAPI, Query
from pathlib import Path
from typing import List, Dict

from app.shroomloc import get_mushrooms, get_all_mushrooms

app = FastAPI(
    title="ShroomLoc API",
    version="0.1.0",
    description="Mushroom location and identification API"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "mushrooms_cleaned.json"


@app.get("/mushrooms", response_model=List[Dict])
def mushrooms(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
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
def list_all_mushrooms() -> List[Dict]:
    """
    Return the full list of mushrooms from the dataset.

    Returns:
        List[Dict]: List of all mushrooms with their properties.
    """
    return get_all_mushrooms()
