import unittest
import sys
import os

# Ajouter le répertoire parent au path pour permettre l'import d'app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.shroomloc import get_mushrooms

class TestGetMushrooms(unittest.TestCase):
    """Unit tests for the get_mushrooms function."""

    def test_get_mushrooms_returns_list(self):
        """Test that get_mushrooms returns a list."""
        lat = 47.989921
        lon = 0.29065708
        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")
        self.assertIsInstance(result, list)

    def test_get_mushrooms_items_structure(self):
        """Test that each mushroom has the expected structure."""
        lat = 47.989921
        lon = 0.29065708
        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")
        self.assertGreater(len(result), 0)
        mushroom = result[0]
        self.assertIn("scientific_name", mushroom)
        self.assertIn("common_name", mushroom)
        self.assertIn("edibility", mushroom)
        self.assertIn("image_url", mushroom)

    def test_get_mushrooms_edibility_values(self):
        """Test that the edibility field has valid values."""
        lat = 47.989921
        lon = 0.29065708
        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")
        allowed = {"edible", "poisonous", "toxic", "inedible", "medicinal", "unknown"}
        for mushroom in result:
            self.assertIn(mushroom["edibility"], allowed)

if __name__ == "__main__":
    unittest.main()
