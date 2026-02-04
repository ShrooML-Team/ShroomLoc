# ShroomLoc

ShroomLoc is a Python project and potential API designed to help users identify mushrooms based on their location, season, and local environmental conditions.

---

## Features

- **Location detection:** Automatically determines your approximate location via IP.
- **Weather integration:** Fetches current temperature and humidity using multiple APIs (wttr.in, Open-Meteo).
- **Season detection:** Determines the current season.
- **Biotope estimation:** Suggests probable habitats for mushrooms based on weather, season, and OpenStreetMap data.
- **Mushroom filtering:** Lists mushrooms that match the current conditions (temperature, humidity, season, and habitat).
- **Images:** Retrieves images for mushrooms via iNaturalist.
- **JSON output:** Ready-to-use JSON data for API integration.

---

## Requirements

- Python 3.8+
- Requests library

Install dependencies:
```bash
pip install requests
```

---

## Usage

1. **Run the main program:**
```bash
python shroomloc.py
```

2. **Check the filtered mushrooms:**
The script prints mushrooms that match your local conditions along with their images.

---

## JSON Dataset Structure

Example entry in `mushrooms.json`:
```json
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

---

## Future Plans

- Expose the functionality as a REST API.
- Add more mushrooms to the dataset.
- Improve habitat detection using more granular OSM queries.
- Add image fallback to Wikimedia Commons or Mushroom.ID.



---

Created by Maelig Pesantez.

