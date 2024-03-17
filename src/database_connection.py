import csv
import requests
from sqlalchemy import Column, Integer, String, create_engine, Table, MetaData
from sqlalchemy.sql import text


# Define the database connection
engine = create_engine('sqlite:///my_database.db')

# Define the metadata
metadata = MetaData()

# Define the table structure
my_table = Table('charge_stations', metadata,
                 # Define your table columns here
                 Column('fuel_type_code', String),
                 Column('station_name', String),
                 Column('street_address', String),
                 Column('intersection_directions', String),
                 Column('city', String),
                 Column('state', String),
                 Column('zip_code', String),
                 Column('plus4', String),
                 Column('station_phone', String),
                 Column('status_code', String),
                 Column('expected_date', String),
                 Column('groups_with_access_code', String),
                 Column('access_days_time', String),
                 Column('cards_accepted', String),
                 Column('bd_blends', String),
                 Column('ng_fill_type_code', String),
                 Column('ng_psi', String),
                 Column('ev_level1_evse_num', String),
                 Column('ev_level2_evse_num', String),
                 Column('ev_dc_fast_count', String),
                 Column('ev_other_info', String),
                 Column('ev_network', String),
                 Column('ev_network_web', String),
                 Column('geocode_status', String),
                 Column('latitude', String),
                 Column('longitude', String),
                 Column('date_last_confirmed', String),
                 Column('station_id', String, primary_key=True),
                 Column('updated_at', String),
                 Column('owner_type_code', String),
                 Column('federal_agency_id', String),
                 Column('federal_agency_name', String),
                 Column('open_date', String),
                 Column('hydrogen_status_link', String),
                 Column('ng_vehicle_class', String),
                 Column('lpg_primary', String),
                 Column('e85_blender_pump', String),
                 Column('ev_connector_types', String),
                 Column('country', String),
                 Column('intersection_directions_french', String),
                 Column('access_days_time_french', String),
                 Column('bd_blends_french', String),
                 Column('groups_with_access_code_french', String),
                 Column('hydrogen_is_retail', String),
                 Column('access_code', String),
                 Column('access_detail_code', String),
                 Column('federal_agency_code', String),
                 Column('facility_type', String),
                 Column('cng_dispenser_num', String),
                 Column('cng_onsite_renewable_source', String),
                 Column('cng_total_compression_capacity', String),
                 Column('cng_storage_capacity', String),
                 Column('lng_onsite_renewable_source', String),
                 Column('e85_other_ethanol_blends', String),
                 Column('ev_pricing', String),
                 Column('ev_pricing_french', String),
                 Column('lpg_nozzle_types', String),
                 Column('hydrogen_pressures', String),
                 Column('hydrogen_standards', String),
                 Column('cng_fill_type_code', String),
                 Column('cng_psi', String),
                 Column('cng_vehicle_class', String),
                 Column('lng_vehicle_class', String),
                 Column('ev_onsite_renewable_source', String),
                 Column('restricted_access', String),
                 Column('rd_blends', String),
                 Column('rd_blends_french', String),
                 Column('rd_blended_with_biodiesel', String),
                 Column('rd_maximum_biodiesel_level', String),
                 Column('nps_unit_name', String),
                 Column('cng_station_sells_renewable_natural_gas', String),
                 Column('lng_station_sells_renewable_natural_gas', String),
                 Column('maximum_vehicle_class', String),
                 Column('ev_workplace_charging', String)
                )

# Define the API endpoint
api_url = '/workspaces/Machine-Learning-Final-Project/electric_stations.csv'

# Fetch data from the API
response = requests.get(api_url)

if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    
    # Bulk insert data into the database
    with engine.connect() as connection:
        # Bulk insert data into the database
        connection.execute(my_table.insert(), data)
else:
    print('Error: Failed to fetch data from API')
