import os
import csv
import requests
from sqlalchemy import Column, Integer, Numeric, Float, String, Date, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


Base = declarative_base()

class Station(Base):
    __tablename__ = 'station'

    id = Column(Integer, primary_key=True, autoincrement=False)
    fuel_type_code = Column(String)
    station_name = Column(String)
    street_address = Column(String)
    intersection_directions = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    plus4 = Column(String)
    station_phone = Column(String)
    status_code = Column(String)
    expected_date = Column(String)
    groups_with_access_code = Column(String)
    access_days_time = Column(String)
    cards_accepted = Column(String)
    bd_blends = Column(String)
    ng_fill_type_code = Column(String)
    ng_psi = Column(String)
    ev_level1_evse_num = Column(Integer)
    ev_level2_evse_num = Column(Integer)
    ev_dc_fast_count = Column(Integer)
    ev_other_info = Column(String)
    ev_network = Column(String)
    ev_network_web = Column(String)
    geocode_status = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    date_last_confirmed = Column(String)
    updated_at = Column(String)
    owner_type_code = Column(String)
    federal_agency_id = Column(String)
    federal_agency_name = Column(String)
    open_date = Column(String)
    hydrogen_status_link = Column(String)
    ng_vehicle_class = Column(String)
    lpg_primary = Column(String)
    e85_blender_pump = Column(String)
    ev_connector_types = Column(String)
    country = Column(String)
    intersection_directions_french = Column(String)
    access_days_time_french = Column(String)
    bd_blends_french = Column(String)
    groups_with_access_code_french = Column(String)
    hydrogen_is_retail = Column(String)
    access_code = Column(String)
    access_detail_code = Column(String)
    federal_agency_code = Column(String)
    facility_type = Column(String)
    cng_dispenser_num = Column(Integer)
    cng_onsite_renewable_source = Column(String)
    cng_total_compression_capacity = Column(Integer)
    cng_storage_capacity = Column(Integer)
    lng_onsite_renewable_source = Column(String)
    e85_other_ethanol_blends = Column(String)
    ev_pricing = Column(String)
    ev_pricing_french = Column(String)
    lpg_nozzle_types = Column(String)
    hydrogen_pressures = Column(String)
    hydrogen_standards = Column(String)
    cng_fill_type_code = Column(String)
    cng_psi = Column(String)
    cng_vehicle_class = Column(String)
    lng_vehicle_class = Column(String)
    ev_onsite_renewable_source = Column(String)
    restricted_access = Column(Boolean)
    rd_blends = Column(String)
    rd_blends_french = Column(String)
    rd_blended_with_biodiesel = Column(String)
    rd_maximum_biodiesel_level = Column(String)
    nps_unit_name = Column(String)
    cng_station_sells_renewable_natural_gas = Column(String)
    lng_station_sells_renewable_natural_gas = Column(String)
    maximum_vehicle_class = Column(String)
    ev_workplace_charging = Column(Boolean)

    def __repr__(self):
        return f"Station(id={self.id}, name='{self.station_name}')"

# Obtener la ruta de la carpeta 'src'
src_dir = os.path.dirname(os.path.abspath(__file__))

# Obtener la ruta de la carpeta 'data' (asumiendo que está al mismo nivel que 'src')
data_dir = os.path.join(os.path.dirname(src_dir), 'data')

# Crear la carpeta 'data' si no existe
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Construir la ruta completa al archivo de la base de datos
db_path = os.path.join(data_dir, 'my_database2.db')

if os.path.exists(db_path):
    os.remove(db_path)

# Crear el archivo de la base de datos si no existe
if not os.path.exists(db_path):
    open(db_path, 'a').close()

# Crear la conexión a la base de datos SQLite
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)  # Crear las tablas en la base de datos
DBSession = sessionmaker(bind=engine)

# API URL
url = "https://developer.nrel.gov/api/alt-fuel-stations/v1.csv"

# Parámetros de la solicitud
params = {
    "api_key": os.environ['API_KEY'],  # Replace your API key on .env,
    "fuel_type": "ELEC",  # Filtra por estaciones eléctricas
    "country": "US",
    "limit": "all"  # Obtiene todos los resultados
}

# Realizamos la solicitud a la API
response = requests.get(url, params=params)

# Comprobamos si la solicitud fue exitosa
if response.status_code == 200:



    # Parseamos la respuesta CSV
    csv_data = response.text

    # Creamos una sesión de base de datos
    session = DBSession()

    # Iteramos sobre cada fila de la respuesta CSV
    csv_reader = csv.DictReader(csv_data.splitlines())
    for row in csv_reader:
        # Creamos una nueva instancia del modelo Station
        station = Station(
            fuel_type_code=row['Fuel Type Code'],
            station_name=row['Station Name'],
            street_address=row['Street Address'],
            intersection_directions=row['Intersection Directions'],
            city=row['City'],
            state=row['State'],
            zip_code=row['ZIP'],
            plus4=row['Plus4'],
            station_phone=row['Station Phone'],
            status_code=row['Status Code'],
            expected_date=row['Expected Date'],
            groups_with_access_code=row['Groups With Access Code'],
            access_days_time=row['Access Days Time'],
            cards_accepted=row['Cards Accepted'],
            bd_blends=row['BD Blends'],
            ng_fill_type_code=row['NG Fill Type Code'],
            ng_psi=row['NG PSI'],
            ev_level1_evse_num=row['EV Level1 EVSE Num'],
            ev_level2_evse_num=row['EV Level2 EVSE Num'],
            ev_dc_fast_count=row['EV DC Fast Count'],
            ev_other_info=row['EV Other Info'],
            ev_network=row['EV Network'],
            ev_network_web=row['EV Network Web'],
            geocode_status=row['Geocode Status'],
            latitude=float(row['Latitude']),
            longitude=float(row['Longitude']),
            date_last_confirmed=row['Date Last Confirmed'],
            id=int(row['ID']),
            updated_at=row['Updated At'],
            owner_type_code=row['Owner Type Code'],
            federal_agency_id=row['Federal Agency ID'],
            federal_agency_name=row['Federal Agency Name'],
            open_date=row['Open Date'],
            hydrogen_status_link=row['Hydrogen Status Link'],
            ng_vehicle_class=row['NG Vehicle Class'],
            lpg_primary=row['LPG Primary'],
            e85_blender_pump=row['E85 Blender Pump'],
            ev_connector_types=row['EV Connector Types'],
            country=row['Country'],
            intersection_directions_french=row['Intersection Directions (French)'],
            access_days_time_french=row['Access Days Time (French)'],
            bd_blends_french=row['BD Blends (French)'],
            groups_with_access_code_french=row['Groups With Access Code (French)'],
            hydrogen_is_retail=row['Hydrogen Is Retail'],
            access_code=row['Access Code'],
            access_detail_code=row['Access Detail Code'],
            federal_agency_code=row['Federal Agency Code'],
            facility_type=row['Facility Type'],
            cng_dispenser_num=row['CNG Dispenser Num'],
            cng_onsite_renewable_source=row['CNG On-Site Renewable Source'],
            cng_total_compression_capacity=row['CNG Total Compression Capacity'],
            cng_storage_capacity=row['CNG Storage Capacity'],
            lng_onsite_renewable_source=row['LNG On-Site Renewable Source'],
            e85_other_ethanol_blends=row['E85 Other Ethanol Blends'],
            ev_pricing=row['EV Pricing'],
            ev_pricing_french=row['EV Pricing (French)'],
            lpg_nozzle_types=row['LPG Nozzle Types'],
            hydrogen_pressures=row['Hydrogen Pressures'],
            hydrogen_standards=row['Hydrogen Standards'],
            cng_fill_type_code=row['CNG Fill Type Code'],
            cng_psi=row['CNG PSI'],
            cng_vehicle_class=row['CNG Vehicle Class'],
            lng_vehicle_class=row['LNG Vehicle Class'],
            ev_onsite_renewable_source=row['EV On-Site Renewable Source'],
            restricted_access=bool(row['Restricted Access']),
            rd_blends=row['RD Blends'],
            rd_blends_french=row['RD Blends (French)'],
            rd_blended_with_biodiesel=row['RD Blended with Biodiesel'],
            rd_maximum_biodiesel_level=row['RD Maximum Biodiesel Level'],
            nps_unit_name=row['NPS Unit Name'],
            cng_station_sells_renewable_natural_gas=row['CNG Station Sells Renewable Natural Gas'],
            lng_station_sells_renewable_natural_gas=row['LNG Station Sells Renewable Natural Gas'],
            maximum_vehicle_class=row['Maximum Vehicle Class'],
            ev_workplace_charging=bool(row['EV Workplace Charging'])
        )

        # Agregamos la nueva estación a la sesión
        session.add(station)

    # Confirmamos los cambios en la base de datos
    session.commit()

else:
    print('Error: Failed to fetch data from API')