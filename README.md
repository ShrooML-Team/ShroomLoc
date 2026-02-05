# ShroomLoc 

ShroomLoc is a **Dockerized REST API** built with **FastAPI** that helps
identify mushrooms based on geographic location and environmental
conditions.

It relies on a curated mushroom JSON dataset including scientific and
common names, edibility, seasonality, temperature and humidity
preferences, habitats, and notes.

------------------------------------------------------------------------

## Features

-   **REST API (FastAPI)**
-   **Docker-ready**
-   **Location-based mushroom suggestion**
-   **Weather integration** (wttr.in, Open-Meteo)
-   **Season detection**
-   **Biotope estimation** using weather + OpenStreetMap
-   **Mushroom filtering** (temperature, humidity, season, habitat)
-   **Image retrieval** via iNaturalist
-   **Swagger documentation** (`/docs`)

------------------------------------------------------------------------

## API Endpoints

### `GET /mushrooms`

Returns mushrooms matching environmental conditions at a given location.

**Query parameters** - `latitude` (float, required) - `longitude`
(float, required)

**Example**

    GET /mushrooms?latitude=47.989921&longitude=0.29065708

------------------------------------------------------------------------

### `GET /mushrooms/all`

Returns the complete mushroom dataset.

**Example**

    GET /mushrooms/all

------------------------------------------------------------------------

## 🐳 Docker Usage

### Build the image

``` bash
docker build -t shroomloc-api .
```

### Run the container

``` bash
docker run -p 8000:8000 shroomloc-api
```

### Access API

-   Swagger UI: http://127.0.0.1:8000/docs
-   API root: http://127.0.0.1:8000

------------------------------------------------------------------------

## Local Development (without Docker)

### Requirements

-   Python 3.9+
-   pip

### Install dependencies

``` bash
pip install -r requirements.txt
```

### Run API

``` bash
uvicorn app.main:app --reload
```

------------------------------------------------------------------------

## Project Structure

    shroomloc/
    ├── app/
    │   ├── main.py
    │   ├── shroomloc.py
    │   ├── mushrooms_cleaned.json
    │   └── __init__.py
    ├── tests/
    │   └── test_shroomloc.py
    ├── utils/
    ├── Dockerfile
    ├── README.md

------------------------------------------------------------------------

## Dataset Structure

Example entry in `mushrooms_cleaned.json`:

``` json
{
  "scientific_name": "Pleurotus ostreatus",
  "common_name": "Pleurote en huître",
  "edibility": "edible",
  "season": ["autumn", "winter"],
  "min_temp": 5,
  "max_temp": 20,
  "min_humidity": 75,
  "habitat": ["bois mort", "troncs", "souches"],
  "notes": "Souvent trouvé sur bois mort."
}
```

------------------------------------------------------------------------

## Future Plans

-   Pagination & filtering for `/mushrooms/all`
-   Pydantic response models
-   API versioning (`/v1`)
-   Caching external API calls
-   Auth & rate limiting
-   Public deployment

------------------------------------------------------------------------

Created by **Maelig Pesantez**
