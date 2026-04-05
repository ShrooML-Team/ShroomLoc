from datetime import datetime
from unittest.mock import Mock
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.shroomloc import (
    determine_biotope,
    filter_mushrooms,
    get_mushroom_details_by_name,
    get_mushroom_recipe,
    get_season,
)


def test_get_season_by_month_boundaries():
    assert get_season(datetime(2026, 1, 15)) == "winter"
    assert get_season(datetime(2026, 4, 15)) == "spring"
    assert get_season(datetime(2026, 7, 15)) == "summer"
    assert get_season(datetime(2026, 10, 15)) == "autumn"


def test_determine_biotope_rules_cover_all_seasons():
    assert determine_biotope(15, 80, "spring") == "forêt de feuillus"
    assert determine_biotope(15, 50, "spring") == "lisière"
    assert determine_biotope(5, 60, "winter") == "bois mort"
    assert determine_biotope(30, 40, "summer") == "prairie"
    assert determine_biotope(22, 40, "summer") == "forêt mixte"
    assert determine_biotope(12, 75, "autumn") == "forêt de feuillus"


def test_filter_mushrooms_uses_habitat_compatibility():
    mushrooms = [
        {
            "scientific_name": "A",
            "common_name": "A",
            "min_temp": 10,
            "max_temp": 25,
            "min_humidity": 50,
            "season": ["autumn"],
            "habitat": ["forêt de feuillus"],
        },
        {
            "scientific_name": "B",
            "common_name": "B",
            "min_temp": 10,
            "max_temp": 25,
            "min_humidity": 50,
            "season": ["summer"],
            "habitat": ["prairie"],
        },
    ]

    # "forêt" is compatible with "forêt de feuillus" per HABITAT_COMPAT.
    result = filter_mushrooms(
        mushrooms,
        temperature=18,
        humidity=70,
        season="autumn",
        biotope="forêt",
    )

    assert len(result) == 1
    assert result[0]["scientific_name"] == "A"


def test_get_mushroom_recipe_returns_none_when_no_meals(monkeypatch):
    first_response = Mock()
    first_response.json.return_value = {"meals": None}

    monkeypatch.setattr("app.shroomloc.requests.get", lambda *args, **kwargs: first_response)

    assert get_mushroom_recipe() is None


def test_get_mushroom_details_by_name_adds_image_and_recipe(tmp_path, monkeypatch):
    sample_json = tmp_path / "mushrooms.json"
    sample_json.write_text(
        """
[
  {
    "scientific_name": "Pleurotus ostreatus",
    "common_name": "Pleurote",
    "edibility": "edible",
    "toxicity": "none",
    "psychoactive": false
  }
]
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.setattr("app.shroomloc.get_mushroom_image", lambda _name: "http://img")
    monkeypatch.setattr("app.shroomloc.get_mushroom_recipe", lambda: {"name": "Soup"})

    details = get_mushroom_details_by_name("pleurotus ostreatus", json_path=str(sample_json))

    assert details is not None
    assert details["image_url"] == "http://img"
    assert details["recipe"] == {"name": "Soup"}
