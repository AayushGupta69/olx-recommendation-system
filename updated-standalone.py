import json

# Load JSON Data from Files
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Filter Packs Based on Budget and Type
def filter_packs(pack_data, pack_name, budget, dynamic_range_factor=0.2):
    """
    Filters packs based on user budget and pack type.

    Parameters:
        pack_data (dict): The JSON data of packs.
        pack_name (str): The name of the pack (single or combination).
        budget (int): The user's budget.
        dynamic_range_factor (float): Percentage factor for dynamic range calculation (default: 20%).

    Returns:
        dict: Filtered results with matching packs.
    """
    packs = pack_data["Packs"]
    pack_names = pack_name.split(" + ")
    results = {}

    # Calculate dynamic range based on budget
    dynamic_range = budget * dynamic_range_factor
    lower_limit = budget - dynamic_range
    upper_limit = budget + dynamic_range

    if len(pack_names) == 1:
        # Single Pack: Filter based on the dynamic range
        for pack in packs:
            if pack_names[0] in pack:
                results["Pack Name"] = pack_names[0]
                results["Budget Range"] = (lower_limit, upper_limit)
                results["Matching Packs"] = [
                    p for p in pack[pack_names[0]] if lower_limit <= p.get("Pack Value", 0) <= upper_limit
                ]
    else:
        # Combination of Packs: Split budget and dynamically calculate ranges
        primary_budget = 0.75 * budget
        secondary_budget = 0.25 * budget

        primary_lower_limit = primary_budget - (primary_budget * dynamic_range_factor)
        primary_upper_limit = primary_budget + (primary_budget * dynamic_range_factor)

        secondary_lower_limit = secondary_budget - (secondary_budget * dynamic_range_factor)
        secondary_upper_limit = secondary_budget + (secondary_budget * dynamic_range_factor)

        results["Pack Name"] = pack_name
        for pack in packs:
            if pack_names[0] in pack:
                results["Primary Pack"] = {
                    "Name": pack_names[0],
                    "Budget": primary_budget,
                    "Dynamic Range": (primary_lower_limit, primary_upper_limit),
                    "Matching Packs": [
                        p for p in pack[pack_names[0]] if primary_lower_limit <= p.get("Pack Value", 0) <= primary_upper_limit
                    ],
                }
            if pack_names[1] in pack:
                results["Secondary Pack"] = {
                    "Name": pack_names[1],
                    "Budget": secondary_budget,
                    "Dynamic Range": (secondary_lower_limit, secondary_upper_limit),
                    "Matching Packs": [
                        p for p in pack[pack_names[1]] if secondary_lower_limit <= p.get("Pack Value", 0) <= secondary_upper_limit
                    ],
                }

    return results

# Example Usage
pack_file = "./json/standalone-packs.json"  # Replace with the path to your JSON file
pack_data = load_json(pack_file)

# Inputs
pack_name = "Limit + BTT"  # Example: Single ("Limit") or Combination ("Limit + BTT")
budget = 10000  # Example budget

# Filter and Display Results
result = filter_packs(pack_data, pack_name, budget)
print(json.dumps(result, indent=4))
