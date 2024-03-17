#Esto es una prueba de control de versiones. Marzo 17, 17:49pm MX
import os
import datetime
import requests

# Function to write to the log file
def write_to_log(message):
    with open("api_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.datetime.now()} - {message}\n")

# Function to delete rows with more fields than expected from a CSV file
def delete_invalid_rows(csv_file, expected_fields):
    # Read the contents of the CSV file using DictReader
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Filter out rows with more fields than expected
    valid_rows = [row for row in rows if len(row) == expected_fields]

    # Write the valid rows back to the CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
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

# Print the response status code
print(f"Response status code: {response.status_code}")

# Check if the request was successful
if response.status_code == 200:
    # Define the directory to save the files
    directory = 'data/raw'
    os.makedirs(directory, exist_ok=True)

    # Write the response content to a CSV file in the specified directory
    csv_file_path = os.path.join(directory, "electric_stations.csv")
    print(f"CSV file path: {csv_file_path}")
    try:
        with open(csv_file_path, "wb") as csv_file:
            csv_file.write(response.content)

        print(f"Data stored in {csv_file_path}")
        write_to_log("API request completed successfully")

    except Exception as e:
        print(f"Error writing data to CSV file: {e}")
else:
    print(f"Error fetching data: {response.status_code}")
    print("Error message:", response.text)
    write_to_log(f"Error fetching data: {response.status_code}. Error message: {response.text}")

