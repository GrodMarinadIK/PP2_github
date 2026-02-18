import json
import os

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'sample-data.json')

# Reading JSON Files
# Using 'with' is best practice for files
with open(file_path, "r") as file:
    # json.load() reads from a file object
    data = json.load(file)

# --- Header of the table ---
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 50, "-" * 20, "-" * 7, "-" * 6)

# Working with JSON data (sample-data.json)
# The data is inside data['imdata'] which is a list
for item in data["imdata"]:
    # Navigating the nested structure: l1PhysIf -> attributes
    attrs = item["l1PhysIf"]["attributes"]
    
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")
    
    # Printing with aligned columns
    print(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<6}")

# Writing JSON Files (Saving the parsed data to a new file)
with open("Practice4\json\parsed_output.json", "w") as outfile:
    json.dump(data, outfile, indent=4)