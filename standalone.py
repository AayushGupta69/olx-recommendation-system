import json

# Load JSON Data from Files
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Filter Packs Based on Budget and Type
def filter_packs(pack_data, pack_name, budget):
    packs = pack_data["Packs"]
    pack_names = pack_name.split(" + ")
    results = {}

    if len(pack_names) == 1:
        # Single Pack: Define budget range
        lower_limit = budget - 5000
        upper_limit = budget + 5000
        for pack in packs:
            if pack_names[0] in pack:
                results["Pack Name"] = pack_names[0]
                results["Budget Range"] = (lower_limit, upper_limit)
                results["Matching Packs"] = [
                    p for p in pack[pack_names[0]] if lower_limit <= p.get("Pack Value", 0) <= upper_limit
                ]
    else:
        # Combination of Packs: Split budget
        primary_budget = 0.75 * budget
        secondary_budget = 0.25 * budget
        results["Pack Name"] = pack_name
        for pack in packs:
            if pack_names[0] in pack:
                results["Primary Pack"] = {
                    "Name": pack_names[0],
                    "Budget": primary_budget,
                    "Matching Packs": [
                        p for p in pack[pack_names[0]] if primary_budget - 5000 <= p.get("Pack Value", 0) <= primary_budget + 5000
                    ],
                }
            if pack_names[1] in pack:
                results["Secondary Pack"] = {
                    "Name": pack_names[1],
                    "Budget": secondary_budget,
                    "Matching Packs": [
                        p for p in pack[pack_names[1]] if secondary_budget - 5000 <= p.get("Pack Value", 0) <= secondary_budget + 5000
                    ],
                }

    return results

# Example Usage
pack_file = "./json/standalone-packs.json"  # Replace with the path to your JSON file
pack_data = load_json(pack_file)

# Inputs
pack_name = "Limit + BTT"  # Example: Single ("Limit") or Combination ("Limit + BTT")
budget = 15000  # Example budget

# Filter and Display Results
result = filter_packs(pack_data, pack_name, budget)
print(json.dumps(result, indent=4))
