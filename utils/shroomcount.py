import json
from collections import Counter, defaultdict
from typing import List, Dict


def load_mushrooms(file_path: str) -> List[Dict]:
    """
    Load mushrooms from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        List[Dict]: List of mushrooms as dictionaries.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def count_habitats(mushrooms: List[Dict]) -> Counter:
    """
    Count occurrences of all habitats in the dataset.

    Args:
        mushrooms (List[Dict]): List of mushrooms.

    Returns:
        Counter: Habitat counts.
    """
    all_habitats = []
    for champ in mushrooms:
        all_habitats.extend(champ.get("habitat", []))
    return Counter(all_habitats)


def find_duplicates(mushrooms: List[Dict]) -> Dict[str, List[str]]:
    """
    Find duplicate scientific and common names in the dataset.

    Args:
        mushrooms (List[Dict]): List of mushrooms.

    Returns:
        Dict[str, List[str]]: Duplicates by 'scientific' and 'common' name.
    """
    scientific_names = [champ["scientific_name"] for champ in mushrooms]
    common_names = [champ["common_name"] for champ in mushrooms]

    scientific_duplicates = [name for name, count in Counter(scientific_names).items() if count > 1]
    common_duplicates = [name for name, count in Counter(common_names).items() if count > 1]

    return {
        "scientific": scientific_duplicates,
        "common": common_duplicates
    }


def categorize_by_edibility(mushrooms: List[Dict]) -> Dict[str, List[str]]:
    """
    Categorize mushrooms by edibility.

    Args:
        mushrooms (List[Dict]): List of mushrooms.

    Returns:
        Dict[str, List[str]]: Keys 'edible' and 'non_edible' with lists of common names.
    """
    categories = defaultdict(list)
    for champ in mushrooms:
        edibility = champ.get("edibility", "unknown").lower()
        common_name = champ.get("common_name", "N/A")
        if edibility in ["edible", "comestible"]:
            categories["edible"].append(common_name)
        else:
            categories["non_edible"].append(common_name)

    categories["edible"].sort()
    categories["non_edible"].sort()
    return categories


def main():
    """
    Load mushrooms, count habitats, find duplicates, and categorize by edibility.
    Prints a summary in English.
    """
    mushrooms = load_mushrooms("../app/mushrooms_cleaned.json")
    print(f"Total mushrooms loaded: {len(mushrooms)}")

    habitat_counts = count_habitats(mushrooms)
    print("\nHabitats found (with occurrences):")
    for habitat, count in habitat_counts.most_common():
        print(f"- {habitat}: {count} times")

    duplicates = find_duplicates(mushrooms)
    print("\nDuplicate scientific names:", duplicates["scientific"] if duplicates["scientific"] else "None")
    print("Duplicate common names:", duplicates["common"] if duplicates["common"] else "None")

    categories = categorize_by_edibility(mushrooms)
    print("\nEdible mushrooms:")
    for name in categories["edible"]:
        print(f"- {name}")

    print("\nNon-edible mushrooms (toxic or inedible):")
    for name in categories["non_edible"]:
        print(f"- {name}")


if __name__ == "__main__":
    main()
