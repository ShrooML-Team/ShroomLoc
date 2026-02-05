import unittest

from app.shroomloc import get_mushrooms


class TestGetMushrooms(unittest.TestCase):

    def test_get_mushrooms_returns_list(self):
        lat = 47.989921
        lon = 0.29065708

        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")

        self.assertIsInstance(result, list)

    def test_get_mushrooms_items_structure(self):
        lat = 47.989921
        lon = 0.29065708

        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")

        # on s'attend à au moins un résultat
        self.assertGreater(len(result), 0)

        mushroom = result[0]

        self.assertIn("scientific_name", mushroom)
        self.assertIn("common_name", mushroom)
        self.assertIn("edibility", mushroom)
        self.assertIn("image_url", mushroom)

    def test_get_mushrooms_edibility_values(self):
        lat = 47.989921
        lon = 0.29065708

        result = get_mushrooms(lat, lon, "./app/mushrooms_cleaned.json")

        allowed = {"edible", "poisonous", "non-edible"}

        for mushroom in result:
            self.assertIn(mushroom["edibility"], allowed)


if __name__ == "__main__":
    unittest.main()
