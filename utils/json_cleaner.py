import json
from collections import Counter

INPUT_FILE = "mushrooms.json"
OUTPUT_FILE = "mushrooms_cleaned.json"

HABITAT_MAP = {
    "pins": "forêt de conifères",
    "forêt de pins": "forêt de conifères",
    "forêts de pins": "forêt de conifères",
    "forêts de conifères": "forêt de conifères",
    "pieds de conifères": "forêt de conifères",

    "forêt de feuillus": "forêt de feuillus",
    "forêts de feuillus": "forêt de feuillus",
    "forêts feuillues": "forêt de feuillus",
    "forêts de chênes": "forêt de feuillus",
    "chênaie": "forêt de feuillus",
    "chênaies": "forêt de feuillus",
    "hêtraie": "forêt de feuillus",
    "hêtraies": "forêt de feuillus",
    "forêts de bouleaux": "forêt de feuillus",

    "forêt mixte": "forêt mixte",
    "forêts mixtes": "forêt mixte",

    "prairies": "prairie",
    "prés": "prairie",
    "pelouses": "prairie",
    "friches": "prairie",

    "lisière": "lisière",
    "lisières": "lisière",
    "lisières de forêt": "lisière",

    "bois mort": "bois mort",
    "bois morts": "bois mort",
    "troncs": "bois mort",
    "troncs de feuillus": "bois mort",
    "souches": "bois mort",
    "souches de feuillus": "bois mort",
    "arbres": "bois mort",

    "zones urbaines": "zones urbaines",

    "litière": "sol",
    "sol sablonneux": "sol"
}


def normalize_habitat(habitat):
    h = habitat.strip().lower()
    return HABITAT_MAP.get(h, h)


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

print("✅ Nettoyage terminé")
print("\n--- Habitats AVANT ---")
for h, c in before_counter.most_common():
    print(f"{h}: {c}")

print("\n--- Habitats APRÈS ---")
for h, c in after_counter.most_common():
    print(f"{h}: {c}")
