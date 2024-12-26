import json

# Load JSON Data from Files
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Filter Packs Based on Pack Names, Sizes, and Durations
def filter_packs_by_criteria(pack_data, pack_names, sizes, durations):
    packs = pack_data["Packs"]
    results = {"Pack Names": pack_names, "Sizes": sizes, "Durations": durations, "Matching Packs": []}

    for i, pack_name in enumerate(pack_names):
        size = sizes[i]
        duration = durations[i]
        matching_packs = []

        for pack in packs:
            if pack_name in pack:
                matching_packs = [
                    p for p in pack[pack_name]
                    if p.get("Size") == size and p.get("Validity") == duration
                ]
                if matching_packs:
                    results["Matching Packs"].append({
                        "Pack Name": pack_name,
                        "Size": size,
                        "Duration": duration,
                        "Matching Packs": matching_packs
                    })

    return results

# Example Usage
pack_file = "./json/standalone-packs.json"  # Replace with the path to your JSON file
pack_data = load_json(pack_file)

# User Inputs
pack_names = ["Limit", "BTT"]           # Example combination of pack names
sizes = [50, 100]                      # Corresponding sizes for each pack
durations = ["30 days", "60 days"]     # Corresponding durations for each pack

# Filter and Display Results
result = filter_packs_by_criteria(pack_data, pack_names, sizes, durations)
print(json.dumps(result, indent=4))
