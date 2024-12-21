import json

def load_json(file_path):
    """
    Load JSON data from a file.
    
    Args:
        file_path (str): Path to the JSON file.
        
    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def find_packs(data, combo_type, budget, range_val=5000):
    """
    Find packs within the specified budget range for a given combo type.
    
    Args:
        data (dict): The JSON data loaded from the file.
        combo_type (str): The name of the combo type.
        budget (int): The user's budget.
        range_val (int): The range around the budget (default is 5000).
        
    Returns:
        list: A list of packs matching the criteria.
    """
    budget_min = budget - range_val
    budget_max = budget + range_val

    # Locate the specific combo type
    for combo in data["Bulk Combos"]:
        if combo_type in combo:
            packs = combo[combo_type]
            # Filter packs within the budget range
            result = [
                pack for pack in packs
                if budget_min <= pack["Incl Add discount - Pack Value"] <= budget_max
            ]
            return result
    return []

# Example Usage
file_path = "./json/bulk-combo-packs.json"  # Replace with the path to your JSON file
data = load_json(file_path)

combo_type = "Mahacombo Power Listing (4D)"  # Replace with desired combo type
user_budget = 140000  # Replace with the user's budget
budget_range = 40000  # ± range for budget

# Find matching packs
matching_packs = find_packs(data, combo_type, user_budget, budget_range)

# Display results
if matching_packs:
    print(f"Packs in '{combo_type}' within the budget range ({user_budget - budget_range} to {user_budget + budget_range}):")
    for pack in matching_packs:
        print(json.dumps(pack, indent=4))
else:
    print(f"No packs found in '{combo_type}' within the budget range ({user_budget - budget_range} to {user_budget + budget_range}).")
