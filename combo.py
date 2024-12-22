import json

def filter_combos(json_file, combo_type, user_budget, budget_range):
    try:
        # Load the JSON data from file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Find the matching combo type
        for combo_category in data['Combos']:
            if combo_type in combo_category:
                combos = combo_category[combo_type]
                break
        else:
            return f"Combo type '{combo_type}' not found."

        # Calculate budget range
        min_budget = user_budget - budget_range
        max_budget = user_budget + budget_range

        # Filter combos within the budget range
        filtered_combos = [
            combo for combo in combos
            if min_budget <= combo["Discounted Packs"] <= max_budget
        ]

        # Display results
        if filtered_combos:
            print(f"Combos in '{combo_type}' within the budget range ({min_budget} - {max_budget}):\n")
            for combo in filtered_combos:
                print(json.dumps(combo, indent=4))
        else:
            print(f"No combos found in '{combo_type}' within the budget range ({min_budget} - {max_budget}).")

    except FileNotFoundError:
        print(f"File '{json_file}' not found.")
    except KeyError as e:
        print(f"Invalid JSON structure: Missing key {e}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
json_file = './json/combo-packs.json'  # Replace with the path to your JSON file
combo_type = "Power Listing (4D) + FA 30 Days combos"  # Specify the combo type
user_budget = 58100  # User's budget
budget_range = 15000  # Range around the budget

filter_combos(json_file, combo_type, user_budget, budget_range)
