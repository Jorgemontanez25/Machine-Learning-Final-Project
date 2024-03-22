import os
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Configuring logging
logging.basicConfig(filename='web_scraping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initiating logging
logging.info('Starting the web scraping script...')

# Getting the current directory path
raw_data_dir = '/workspaces/Machine-Learning-Final-Project/data/raw'  # Directory for raw data

# Navigating to the webpage
url = "https://www.census.gov/geographies/reference-files/2010/geo/state-area.html"
response = requests.get(url)

# Checking if the request was successful
if response.status_code == 200:
    logging.info(f'Loading webpage: {url}')
    
    # Parsing the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Finding the table containing state areas
    table = soup.find('table')
    
    # Checking if the table was found
    if table:
        logging.info('Table found. Extracting data...')
        
        # Extracting data from the table
        data = []
        columns_to_extract = ['State and other areas', 'Total Area', 'Land Area', 'Water Area']
        for row in table.find_all('tr'):
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            extracted_row = [row_data[0]] + row_data[1:5]  # Extracting the specified columns
            data.append(extracted_row)
        
        # Logging the extracted data
        for row in data:
            logging.info(f'Data row: {row}')
        
        # Creating a DataFrame from the extracted data
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Saving the DataFrame as a CSV file
        csv_path = os.path.join(raw_data_dir, 'States_Areas.csv')
        df.to_csv(csv_path, index=False)
        
        logging.info(f'Data saved successfully to: {csv_path}')
    else:
        logging.error('Table not found on the webpage.')
else:
    logging.error(f'Failed to load webpage: {url}, Status code: {response.status_code}')
