import json
from collections import Counter

INPUT_FILE = "../mushrooms.json"
OUTPUT_FILE = "../mushrooms_cleaned.json"

HABITAT_MAP = {
    "pins": "coniferous forest",
    "forêt de pins": "coniferous forest",
    "forêts de pins": "coniferous forest",
    "forêts de conifères": "coniferous forest",
    "pieds de conifères": "coniferous forest",

    "forêt de feuillus": "deciduous forest",
    "forêts de feuillus": "deciduous forest",
    "forêts feuillues": "deciduous forest",
    "forêts de chênes": "deciduous forest",
    "chênaie": "deciduous forest",
    "chênaies": "deciduous forest",
    "hêtraie": "deciduous forest",
    "hêtraies": "deciduous forest",
    "forêts de bouleaux": "deciduous forest",

    "forêt mixte": "mixed forest",
    "forêts mixtes": "mixed forest",

    "prairies": "meadow",
    "prés": "meadow",
    "pelouses": "meadow",
    "friches": "meadow",

    "lisière": "forest edge",
    "lisières": "forest edge",
    "lisières de forêt": "forest edge",

    "bois mort": "dead wood",
    "bois morts": "dead wood",
    "troncs": "dead wood",
    "troncs de feuillus": "dead wood",
    "souches": "dead wood",
    "souches de feuillus": "dead wood",
    "arbres": "dead wood",

    "zones urbaines": "urban areas",

    "litière": "soil",
    "sol sablonneux": "soil"
}


def normalize_habitat(habitat: str) -> str:
    """
    Normalize a habitat string based on the predefined HABITAT_MAP.
    Returns the mapped habitat if it exists, otherwise returns the cleaned string.
    """
    h = habitat.strip().lower()
    return HABITAT_MAP.get(h, h)


def main():
    """
    Load mushrooms JSON, normalize habitats, count occurrences before and after normalization,
    and save the cleaned dataset.
    """
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    before_counter = Counter()
    after_counter = Counter()

    for champ in data:
        new_habitats = set()
        for h in champ.get("habitat", []):
            before_counter[h] += 1
            normalized = normalize_habitat(h)
            new_habitats.add(normalized)
            after_counter[normalized] += 1
        champ["habitat"] = sorted(new_habitats)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Cleaning completed")
    print("\n--- Habitats BEFORE ---")
    for h, c in before_counter.most_common():
        print(f"{h}: {c}")

    print("\n--- Habitats AFTER ---")
    for h, c in after_counter.most_common():
        print(f"{h}: {c}")


if __name__ == "__main__":
    main()
