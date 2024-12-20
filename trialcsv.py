import csv
import json
from datetime import datetime

# Input and output file paths
input_csv_file = "daily.csv"
output_json_file = "output.json"

# Function to convert the CSV to JSON
def csv_to_json(csv_file, json_file):
    data = []
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            date = datetime.strptime(row[0], "%d/%m/%y").strftime("%d/%m/%Y")  # Convert date format
            amount = float(row[1].replace(",", "").replace('"', ""))  # Convert amount to float
            reason = row[2].strip() if row[2] else None  # Handle empty reasons

            # Append formatted entry to the list
            data.append({
                "date": date,
                "amount": round(amount, 2),
                "category": None,
                "reason": reason
            })

    # Write the JSON output
    with open(json_file, mode='w') as file:
        json.dump(data, file, indent=4)

# Call the function
csv_to_json(input_csv_file, output_json_file)
print(f"Data has been successfully converted and saved to {output_json_file}.")