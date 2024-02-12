import json
from pathlib import Path

# Construct the path to data.json
json_file_path = Path(__file__).resolve().parent / "data" / "data.json"

# Read the content of data.json
with open(json_file_path, "a") as file:
    # Attempt to read existing content (if any)
    # file.seek(0)
    # for line in file:
    #     print(line)
    existing_data = file.read()
    print(existing_data)
    # return
    # Parse existing JSON data, if any
    # try:
    #     data = json.loads(existing_data)
    # except json.JSONDecodeError:
    #     data = {}

    # Modify the data as needed
    # For example, adding a new key-value pair
    # data["new_key"] = "new_value"

    # Write the modified data back to the file
    # file.seek(0)  # Move the file pointer to the beginning
    # json.dump(data, file, indent=4)  # Write JSON data to the file with indentation
    # file.truncate()
