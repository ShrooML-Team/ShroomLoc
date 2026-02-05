import requests
from datetime import datetime
import random
import os
import json

# -----------------------------
# 1. Mock of localisation
# -----------------------------

def get_approx_location():
    """
    Returns an approximate latitude and longitude based on the user's IP address.
    If the IP-based location cannot be determined, returns default coordinates (Bois de Changé
    """
    try:
        res = requests.get("https://ipinfo.io/json", timeout=5).json()
        loc = res.get("loc", None)
        if loc:
            lat, lon = map(float, loc.split(","))
            print(f"Localisation approximative : lat={lat}, lon={lon}")
            return lat, lon
    except Exception as e:
        print(f"Impossible d'obtenir la localisation depuis IP: {e}")
    
    print("Utilisation de coordonnées par défaut (Bois de Changé)")
    return 47.989921, 0.29065708

# -----------------------------
# 2. Retrival of weather data
# -----------------------------
# Utilisation de OpenWeatherMap (API gratuite nécessite une clé)

def get_weather(lat, lon):
    """
    Returns the current temperature and humidity for the given latitude and longitude.
    Tries multiple APIs for robustness. If all fail, returns default values.
    param lat: Latitude of the location
    param lon: Longitude of the location
    """
    
    apis = [
        "wttr", 
        "open-meteo"
    ]
    
    for api in apis:
        try:
            if api == "wttr":
                url = f"https://wttr.in/{lat},{lon}?format=j1"
                data = requests.get(url, timeout=5).json()
                temp = float(data["current_condition"][0]["temp_C"])
                hum = float(data["current_condition"][0]["humidity"])
                return temp, hum

            elif api == "open-meteo":
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
                data = requests.get(url, timeout=5).json()
                temp = data["current_weather"]["temperature"]
                hum = data["hourly"]["relativehumidity_2m"][0]
                return temp, hum

        except Exception as e:
            continue

    temp = 10.0
    hum = 80.0
    return temp, hum

# -----------------------------
# 3. Determination of the season
# -----------------------------
def get_season(date=None):
    """
    Returns the current season based on the month of the given date.
    param date: Optional datetime object. If None, uses current date.
    """
    if date is None:
        date = datetime.now()
    month = date.month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

# -----------------------------
# 4. Determination of the biotope
# -----------------------------

CANONICAL_HABITATS = {
    "forêt de feuillus",
    "forêt de conifères",
    "forêt mixte",
    "prairie",
    "lisière",
    "bois mort",
    "zones urbaines",
    "sol",
    "forêt"
}

def determine_biotope(temperature, humidity, season):
    """
    Determine a likely biotope based on temperature, humidity, and season.
    This is a heuristic function that can be refined with more complex logic or ML.
    param temperature: Current temperature
    param humidity: Current humidity
    param season: Current season (e.g., 'spring', 'summer', 'autumn', 'winter')
    """
    if humidity >= 75 and temperature <= 15:
        return random.choice(["bois mort", "lisière"])
    
    elif 15 <= temperature <= 25 and 50 <= humidity <= 75:
        return "forêt de conifères"
    
    elif season in ["spring", "autumn"] and 50 <= humidity <= 80:
        return "forêt de feuillus"
    
    elif temperature > 20 and humidity < 70:
        return "prairie"
    
    return random.choice([
        "forêt de feuillus",
        "forêt de conifères",
        "forêt mixte",
        "prairie",
        "lisière",
        "bois mort"
    ])

def refine_biotope_osm(lat, lon):
    """
    Refines the biotope using OpenStreetMap data around the given latitude and longitude.
    param lat: Latitude of the location
    param lon: Longitude of the location
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      way(around:50,{lat},{lon})["landuse"];
      way(around:50,{lat},{lon})["natural"];
    );
    out tags;
    """
    biotope_candidates = []
    try:
        response = requests.get(overpass_url, params={"data": query}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for element in data.get("elements", []):
                tags = element.get("tags", {})
                if tags.get("landuse") == "forest" or tags.get("natural") == "forest":
                    biotope_candidates.append("forêt")
                elif tags.get("landuse") == "meadow":
                    biotope_candidates.append("prairie")
    except requests.exceptions.RequestException:
        pass

    if biotope_candidates:
        biotope = random.choice(biotope_candidates)
        if biotope == "forêt":
            biotope = random.choice([
                "forêt de feuillus",
                "forêt de conifères",
                "forêt mixte"
            ])
        return biotope
    return None


# -----------------------------
# 5. Filtering mushrooms based on conditions
# -----------------------------

def filter_mushrooms(champignons, temperature, humidity, season, biotope):
    """
    Filters the list of mushrooms based on the given environmental conditions.
    param champignons: List of mushroom dicts with keys 'min_temp', 'max_temp', 'min_humidity', 'season', 'habitat'
    param temperature: Current temperature
    param humidity: Current humidity
    param season: Current season (e.g., 'spring', 'summer', 'autumn
    param biotope: Current biotope (e.g., 'forêt de feuillus')
    """
    filtered = []
    for champ in champignons:
        temp_ok = champ["min_temp"] <= temperature <= champ["max_temp"]
        humidity_ok = champ["min_humidity"] <= humidity
        season_ok = season in champ["season"]
        habitat_ok = biotope in champ["habitat"]
        if temp_ok and humidity_ok and season_ok and habitat_ok:
            filtered.append(champ)
    return filtered


# -----------------------------
# 6. Retrieval of mushroom images from iNaturalist
# -----------------------------

def get_mushroom_image(species_name="Amanita muscaria"):
    """
    Returns a URL of an image for the given mushroom species from iNaturalist.
    If no image is found, returns None.
    param species_name: Scientific name of the mushroom species
    """
    url = "https://api.inaturalist.org/v1/observations"
    params = {
        "taxon_name": species_name,
        "photos": "true",
        "per_page": 1,
        "quality_grade": "research"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        results = data.get("results", [])
        if not results:
            return None

        photos = results[0].get("photos", [])
        if not photos:
            return None

        return photos[0]["url"].replace("square", "large")

    except Exception as e:
        print(f"Erreur image iNaturalist pour '{species_name}': {e}")
        return None

# -----------------------------
# 7. Preparation of JSON for API (filtered JSON)
# -----------------------------

def get_mushrooms(lat, lon, file="mushrooms_cleaned.json"):
    """
    Returns a list of mushrooms filtered by environmental conditions at the given latitude and longitude.
    param lat: Latitude of the location
    param lon: Longitude of the location
    param file: Path to the cleaned mushrooms JSON file
    """
    temperature, humidity = get_weather(lat, lon)
    season = get_season()
    biotope = refine_biotope_osm(lat, lon)
    if biotope is None:
        biotope = determine_biotope(temperature, humidity, season)

    with open(file, "r", encoding="utf-8") as f:
        champignons = json.load(f)
    
    filtered = filter_mushrooms(champignons, temperature, humidity, season, biotope)
    
    api_data = []
    if filtered:
        for champ in filtered:
            image_url = get_mushroom_image(champ["scientific_name"])
            api_data.append({
                "scientific_name": champ["scientific_name"],
                "common_name": champ["common_name"],
                "edibility": champ["edibility"],
                "image_url": image_url
            })
    else:
        fallback_species = "Amanita muscaria"
        image_url = get_mushroom_image(fallback_species)
        api_data.append({
            "scientific_name": fallback_species,
            "common_name": "Amanite tue-mouches",
            "edibility": "non-edible",
            "image_url": image_url
        })
    
    return api_data

# ----------------------------------------
# 8. Preparation of cleaned JSON (normalization of habitats)
# ----------------------------------------

def get_all_mushrooms(json_path="app/mushrooms_cleaned.json"):
    """
    Returns the full list of mushrooms from the cleaned JSON file.
    param json_path: Path to the cleaned mushrooms JSON file
    """
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
