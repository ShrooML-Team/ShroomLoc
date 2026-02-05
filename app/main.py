from fastapi import FastAPI, Query
from pathlib import Path

from app.shroomloc import get_mushrooms

app = FastAPI(
    title="ShroomLoc API",
    version="0.1.0",
    description="API de localisation de champignons"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "mushrooms_cleaned.json"


@app.get("/mushrooms")
def mushrooms(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    return get_mushrooms(latitude, longitude, DATA_FILE)
