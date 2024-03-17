import csv
import datetime
import requests

# Function to write to the log file
def write_to_log(message):
    with open("api_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.datetime.now()} - {message}\n")

# Function to delete rows with more fields than expected from a CSV file
def delete_invalid_rows(csv_file, expected_fields):
    # Read the contents of the CSV file into a list of lists
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Filter out rows with more fields than expected
    valid_rows = [row for row in rows if len(row) == expected_fields]

    # Write the valid rows back to the CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(valid_rows)

    print("Invalid rows deleted successfully")

# API URL
url = "https://developer.nrel.gov/api/alt-fuel-stations/v1.csv"

# Request parameters
params = {
    "api_key": "ispXZf0PCuTvLlS4U4heX8t1XxLsfrbq9gKxjcUJ",  # Replace with your API key
    "fuel_type": "ELEC",  # Filter by electric stations
    "country": "US",
    "limit": "all"  # Get all results
 }

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Write the response content to a CSV file
    with open("electric_stations.csv", "w", encoding="utf-8") as csv_file:
        csv_file.write(response.text)

    print("Data stored in electric_stations.csv")
    write_to_log("API request completed successfully")

    # Perform additional operations if needed
    # For example, deleting invalid rows
    delete_invalid_rows("electric_stations.csv", 77)
else:
    print(f"Error fetching data: {response.status_code}")
    print("Error message:", response.text)
    write_to_log(f"Error fetching data: {response.status_code}. Error message: {response.text}")

