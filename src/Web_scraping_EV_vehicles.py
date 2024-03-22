import os
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Configurar el registro (logging)
logging.basicConfig(filename='web_scraping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Agregar un registro para indicar que el script ha comenzado
logging.info('Iniciando el script de web scraping...')

# Obtener la ruta del directorio actual
raw_data_dir = '/workspaces/Machine-Learning-Final-Project/data/raw'  # Directory for raw data

# Navegar a la página web
url = "https://afdc.energy.gov/vehicle-registration"
response = requests.get(url)

# Verificar que la solicitud haya sido exitosa
if response.status_code == 200:
    # Agregar un registro después de la llamada a requests.get(url)
    logging.info(f'Cargando la pagina web: {url}')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar la tabla de registro de vehículos
    table = soup.find('table', id='vehicle_registration')
    
    state_list = []
    electric_list = []
    
    # Extraer datos de la tabla
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 1:
            state = columns[0].text.strip()
            electric = columns[1].text.strip()
            state_list.append(state)
            electric_list.append(electric)

    # Crear DataFrame
    df = pd.DataFrame({'state': state_list, 'electric': electric_list})
    
    # Ruta para guardar el archivo CSV en el directorio '/workspaces/Machine-Learning-Final-Project/data/raw'
    csv_path = os.path.join(raw_data_dir, 'Electric_vehicles_by_state.csv')
    
    # Guardar el DataFrame como CSV
    df.to_csv(csv_path, index=False)

    # Agregar un registro después de guardar el DataFrame
    logging.info(f'Datos guardados exitosamente en {csv_path}')
else:
    logging.error(f'Error al cargar la página web: {url}, Status code: {response.status_code}')


