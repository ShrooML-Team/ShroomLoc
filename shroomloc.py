import requests
from datetime import datetime
import random
import os

# -----------------------------
# 1. Mock de la localisation
# -----------------------------

def get_approx_location():
    """Récupère une localisation approximative depuis l'IP"""
    try:
        # ipinfo.io
        res = requests.get("https://ipinfo.io/json", timeout=5).json()
        loc = res.get("loc", None)
        if loc:
            lat, lon = map(float, loc.split(","))
            print(f"Localisation approximative : lat={lat}, lon={lon}")
            return lat, lon
    except Exception as e:
        print(f"Impossible d'obtenir la localisation depuis IP: {e}")
    
    # fallback sur coordonnées par défaut
    print("Utilisation de coordonnées par défaut (Bois de Changé)")
    return 47.989921, 0.29065708

lat, lon = get_approx_location()


# -----------------------------
# 2. Récupération météo
# -----------------------------
# Utilisation de OpenWeatherMap (API gratuite nécessite une clé)

def get_weather(lat, lon):
    """Récupère température et humidité via plusieurs API sans clé"""
    
    # Liste d'API à tester successivement
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
                print("Météo récupérée via wttr.in")
                return temp, hum

            elif api == "open-meteo":
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
                data = requests.get(url, timeout=5).json()
                temp = data["current_weather"]["temperature"]
                hum = data["hourly"]["relativehumidity_2m"][0]
                print("Météo récupérée via Open-Meteo")
                return temp, hum

        except Exception as e:
            print(f"Échec API {api}: {e}")
            continue

    print("Toutes les API ont échoué, utilisation de valeurs par défaut")
    temp = 10.0
    hum = 80.0
    return temp, hum

temperature, humidity = get_weather(lat, lon)
print(f"Température : {temperature}°C, Humidité : {humidity}%")


# -----------------------------
# 3. Détermination de la saison
# -----------------------------
def get_season(date=None):
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

current_season = get_season()
print(f"Saison actuelle : {current_season}")

# -----------------------------
# 4. Détermination du biotope
# -----------------------------
import random

# Habitats canoniques correspondant à ton dataset
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
    Détermine le biotope le plus probable en fonction de la météo et de la saison,
    aligné avec les habitats canoniques de ton dataset.
    """
    # Bois morts ou lisières humides si forte humidité et basse température
    if humidity >= 75 and temperature <= 15:
        return random.choice(["bois mort", "lisière"])
    
    # Forêt de conifères si température modérée et humidité moyenne
    elif 15 <= temperature <= 25 and 50 <= humidity <= 75:
        return "forêt de conifères"
    
    # Forêt de feuillus si saison printanière ou automnale et humidité moyenne
    elif season in ["spring", "autumn"] and 50 <= humidity <= 80:
        return "forêt de feuillus"
    
    # Prairies si temps chaud et humide modéré
    elif temperature > 20 and humidity < 70:
        return "prairie"
    
    # Fallback aléatoire si aucune condition ne matche parfaitement
    return random.choice([
        "forêt de feuillus",
        "forêt de conifères",
        "forêt mixte",
        "prairie",
        "lisière",
        "bois mort"
    ])


# Overpass API pour raffiner le biotope autour du point (50m radius)
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
        try:
            data = response.json()
            for element in data.get("elements", []):
                tags = element.get("tags", {})
                if tags.get("landuse") == "forest" or tags.get("natural") == "forest":
                    biotope_candidates.append("forêt")
                elif tags.get("landuse") == "meadow":
                    biotope_candidates.append("prairie")
        except ValueError:
            print("Erreur JSON Overpass, fallback sur biotope météo/saison")
    else:
        print(f"Overpass API renvoie le status {response.status_code}, fallback sur biotope météo/saison")
except requests.exceptions.RequestException as e:
    print(f"Erreur requête Overpass: {e}, fallback sur biotope météo/saison")

# Choisir un biotope si OSM a renvoyé quelque chose
if biotope_candidates:
    biotope = random.choice(biotope_candidates)
    # Remplacer le générique "forêt" par un type précis
    if biotope == "forêt":
        biotope = random.choice([
            "forêt de feuillus",
            "forêt de conifères",
            "forêt mixte"
        ])
else:
    # fallback météo/saison
    biotope = determine_biotope(temperature, humidity, current_season)

print(f"Biotope estimé via OSM ou météo : {biotope}")

# -----------------------------
# 5. Filtrage des champignons
# -----------------------------
import json

with open("mushrooms.json", "r", encoding="utf-8") as f:
    champignons = json.load(f)

# Filtrage selon température, humidité, saison et biotope
filtered = []
for champ in champignons:
    temp_ok = champ["min_temp"] <= temperature <= champ["max_temp"]
    humidity_ok = champ["min_humidity"] <= humidity
    season_ok = current_season in champ["season"]
    habitat_ok = biotope in champ["habitat"]
    
    if temp_ok and humidity_ok and season_ok and habitat_ok:
        filtered.append(champ)

print(f"\nChampignons possibles selon la météo et le biotope :")
for champ in filtered:
    print(f"- {champ['common_name']} ({champ['scientific_name']}) [{champ['edibility']}]")


# -----------------------------
# 6. Récupération images via mushroom.id
# -----------------------------
# -----------------------------
# 6. Récupération images via iNaturalist
# -----------------------------

def get_mushroom_image(species_name="Amanita muscaria"):
    """
    Récupère une image depuis iNaturalist à partir du nom scientifique
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

        # Remplace "square" par "medium" ou "large"
        return photos[0]["url"].replace("square", "large")

    except Exception as e:
        print(f"Erreur image iNaturalist pour '{species_name}': {e}")
        return None


print("\nImages associées :")

# Cas 1 : champignons trouvés
if filtered:
    for champ in filtered:
        species = champ["scientific_name"]
        image_url = get_mushroom_image(species)

        if image_url:
            print(f"- {species} → {image_url}")
        else:
            print(f"- {species} → aucune image trouvée")

# Cas 2 : aucun champignon → fallback Amanita muscaria
else:
    fallback_species = "Amanita muscaria"
    image_url = get_mushroom_image(fallback_species)

    if image_url:
        print(f"- {fallback_species} (fallback) → {image_url}")
    else:
        print(f"- {fallback_species} → aucune image trouvée")

# -----------------------------
# 7. Préparation JSON pour API
# -----------------------------

import json

# Crée la liste des champignons avec nom scientifique et image
api_data = []

# Cas 1 : champignons trouvés
if filtered:
    for champ in filtered:
        species = champ["scientific_name"]
        image_url = get_mushroom_image(species)
        api_data.append({
            "scientific_name": species,
            "common_name": champ["common_name"],
            "edibility": champ["edibility"],
            "image_url": image_url if image_url else None
        })

# Cas 2 : aucun champignon → fallback Amanita muscaria
else:
    fallback_species = "Amanita muscaria"
    image_url = get_mushroom_image(fallback_species)
    api_data.append({
        "scientific_name": fallback_species,
        "common_name": "Amanite tue-mouches",
        "edibility": "non-edible",
        "image_url": image_url if image_url else None
    })

# Pour l'instant, on print juste le JSON formaté
api_json = json.dumps(api_data, indent=2, ensure_ascii=False)
print("\nJSON prêt pour API :")
print(api_json)
