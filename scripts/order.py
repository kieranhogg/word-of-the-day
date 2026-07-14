import json

level = "complex"
# 1. Load the existing JSON file
with open(f'data/{level}.json', 'r') as file:
    data = json.load(file)

# 2. Loop through the words array and add an order number
# Using enumerate with start=1 gives us a clean counter
for index, item in enumerate(data['words'], start=1):
    item['order'] = index
    item['level'] = level

# 3. Save the updated data to a new file
with open(f'data/{level}_updated.json', 'w') as file:
    json.dump(data, file, indent=4)

print(f"Successfully added order numbers to {len(data['words'])} entries!")