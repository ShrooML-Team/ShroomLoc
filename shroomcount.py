import json
from collections import Counter, defaultdict

# Chargement du JSON
with open("mushrooms_cleaned.json", "r", encoding="utf-8") as f:
    champignons = json.load(f)

print("Taille de la liste complète des champignons :", len(champignons))

# -----------------------------
# 1. Décompte des habitats
# -----------------------------
all_habitats = []
for champ in champignons:
    all_habitats.extend(champ.get("habitat", []))

habitat_counts = Counter(all_habitats)
print("\nHabitats recensés (avec occurrences) :")
for habitat, count in habitat_counts.most_common():
    print(f"- {habitat}: {count} fois")

# -----------------------------
# 2. Vérification des doublons
# -----------------------------
scientific_names = [champ["scientific_name"] for champ in champignons]
common_names = [champ["common_name"] for champ in champignons]

scientific_duplicates = [name for name, count in Counter(scientific_names).items() if count > 1]
common_duplicates = [name for name, count in Counter(common_names).items() if count > 1]

print("\nDoublons par nom scientifique :", scientific_duplicates if scientific_duplicates else "Aucun doublon")
print("Doublons par nom commun :", common_duplicates if common_duplicates else "Aucun doublon")

# -----------------------------
# 3. Noms communs par comestibilité
# -----------------------------
categories = defaultdict(list)
for champ in champignons:
    edibility = champ.get("edibility", "unknown")
    common_name = champ.get("common_name", "N/A")
    
    if edibility.lower() in ["edible", "comestible"]:
        categories["comestible"].append(common_name)
    else:
        categories["non_comestible"].append(common_name)

# Tri alphabétique
categories["comestible"].sort()
categories["non_comestible"].sort()

print("\nChampignons comestibles :")
for name in categories["comestible"]:
    print(f"- {name}")

print("\nChampignons non comestibles (toxiques ou mortels) :")
for name in categories["non_comestible"]:
    print(f"- {name}")
