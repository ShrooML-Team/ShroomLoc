import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le répertoire parent au path pour permettre l'import d'app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.shroomloc import get_mushrooms

class TestGetMushrooms(unittest.TestCase):
    """Unit tests for the get_mushrooms function."""

    @patch('app.shroomloc.get_weather')
    @patch('app.shroomloc.get_season')
    @patch('app.shroomloc.refine_biotope_osm')
    @patch('app.shroomloc.determine_biotope')
    @patch('app.shroomloc.filter_mushrooms')
    @patch('app.shroomloc.get_mushroom_image')
    def test_get_mushrooms_returns_list(self, mock_image, mock_filter, mock_biotope, mock_osm, mock_season, mock_weather):
        """Test that get_mushrooms returns a list."""
        mock_weather.return_value = (15, 65)
        mock_season.return_value = "autumn"
        mock_osm.return_value = "forest"
        mock_filter.return_value = [
            {
                "scientific_name": "Amanita muscaria",
                "common_name": "Fly Agaric",
                "edibility": "poisonous",
                "toxicity": "high",
                "psychoactive": True
            }
        ]
        mock_image.return_value = "http://example.com/image.jpg"
        
        lat = 47.989921
        lon = 0.29065708
        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")
        self.assertIsInstance(result, list)

    @patch('app.shroomloc.get_weather')
    @patch('app.shroomloc.get_season')
    @patch('app.shroomloc.refine_biotope_osm')
    @patch('app.shroomloc.determine_biotope')
    @patch('app.shroomloc.filter_mushrooms')
    @patch('app.shroomloc.get_mushroom_image')
    def test_get_mushrooms_items_structure(self, mock_image, mock_filter, mock_biotope, mock_osm, mock_season, mock_weather):
        """Test that each mushroom has the expected structure."""
        mock_weather.return_value = (15, 65)
        mock_season.return_value = "autumn"
        mock_osm.return_value = "forest"
        mock_filter.return_value = [
            {
                "scientific_name": "Amanita muscaria",
                "common_name": "Fly Agaric",
                "edibility": "poisonous",
                "toxicity": "high",
                "psychoactive": True
            }
        ]
        mock_image.return_value = "http://example.com/image.jpg"
        
        lat = 47.989921
        lon = 0.29065708
        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")
        self.assertGreater(len(result), 0)
        mushroom = result[0]
        self.assertIn("scientific_name", mushroom)
        self.assertIn("common_name", mushroom)
        self.assertIn("edibility", mushroom)
        self.assertIn("image_url", mushroom)

    @patch('app.shroomloc.get_weather')
    @patch('app.shroomloc.get_season')
    @patch('app.shroomloc.refine_biotope_osm')
    @patch('app.shroomloc.determine_biotope')
    @patch('app.shroomloc.filter_mushrooms')
    @patch('app.shroomloc.get_mushroom_image')
    def test_get_mushrooms_edibility_values(self, mock_image, mock_filter, mock_biotope, mock_osm, mock_season, mock_weather):
        """Test that the edibility field has valid values."""
        mock_weather.return_value = (15, 65)
        mock_season.return_value = "autumn"
        mock_osm.return_value = "forest"
        mock_filter.return_value = [
            {
                "scientific_name": "Amanita muscaria",
                "common_name": "Fly Agaric",
                "edibility": "poisonous",
                "toxicity": "high",
                "psychoactive": True
            }
        ]
        mock_image.return_value = "http://example.com/image.jpg"
        
        lat = 47.989921
        lon = 0.29065708
        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")
        allowed = {"edible", "poisonous", "toxic", "inedible", "medicinal", "unknown"}
        for mushroom in result:
            self.assertIn(mushroom["edibility"], allowed)

if __name__ == "__main__":
    unittest.main()
