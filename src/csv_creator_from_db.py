import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, text

# Define the path to the SQLite database
db_path = 'data/my_database2.db'

# Create engine
engine = create_engine(f'sqlite:///{db_path}')

# Define metadata
metadata = MetaData()

# Reflect database tables
metadata.reflect(bind=engine)

# Create CSV directory if it doesn't exist
csv_dir = '/workspaces/Machine-Learning-Final-Project/data/csv'
os.makedirs(csv_dir, exist_ok=True)

# Load the 'station' table
station_table = Table('station', metadata, autoload=True, autoload_with=engine)

# Load the 'state' table
state_table = Table('state', metadata, autoload=True, autoload_with=engine)

# Load the 'area' table
area_table = Table('area', metadata, autoload=True, autoload_with=engine)

# Load the 'vehicle' table
vehicle_table = Table('vehicle', metadata, autoload=True, autoload_with=engine)

# Create a connection
conn = engine.connect()

# Print the columns of the state table to verify it's properly loaded
print(state_table.columns.keys())

# Define SQL query to group station data by state and calculate aggregated values
query_station = text("""
    SELECT 
        s.state_ab, 
        IFNULL(SUM(CAST(s.ev_level1_evse_num AS INT)), 0) AS Total_EV_Level1_EVSE_Num, 
        IFNULL(SUM(CAST(s.ev_level2_evse_num AS INT)), 0) AS Total_EV_Level2_EVSE_Num, 
        IFNULL(SUM(CAST(s.ev_dc_fast_count AS INT)), 0) AS Total_EV_DC_FastCount, 
        COUNT(DISTINCT(s.id)) AS stations_number,
        t.state_name
    FROM 
        station s
    JOIN 
        state t 
    ON 
        s.state_ab = t.state_ab
    GROUP BY 
        s.state_ab
""")

try:
    # Execute the station query
    result_station = conn.execute(query_station)

    # Fetch the results into a DataFrame
    station_df = pd.DataFrame(result_station.fetchall(), columns=result_station.keys())

    # Define CSV file path for the station data
    station_csv_path = os.path.join(csv_dir, 'station_state_merged.csv')

    # Write the station data to a CSV file
    station_df.to_csv(station_csv_path, index=False)

    print(f'Station-state merged data CSV file created at: {station_csv_path}')

except Exception as e:
    print(f"An error occurred: {e}")

# Define SQL query to join area and vehicle tables based on state_name
query_area_vehicle = text("""
    SELECT 
        a.*,
        v.electric
    FROM 
        area a
    JOIN 
        vehicle v 
    ON 
        a.state_name = v.state_name
""")

# Execute the area and vehicle merged query
result_area_vehicle = conn.execute(query_area_vehicle)

# Fetch the results into a DataFrame
area_vehicle_merged_df = pd.DataFrame(result_area_vehicle.fetchall(), columns=result_area_vehicle.keys())

# Define CSV file path for the merged area and vehicle data
area_vehicle_merged_csv_path = os.path.join(csv_dir, 'area_vehicle_merged.csv')

# Write the merged area and vehicle data to a CSV file
area_vehicle_merged_df.to_csv(area_vehicle_merged_csv_path, index=False)

print(f'Area-vehicle merged data CSV file created at: {area_vehicle_merged_csv_path}')

# Merge the station-state and area-vehicle dataframes on the state_name column
final_merged_df = pd.merge(station_df, area_vehicle_merged_df, on='state_name', how='inner')

# Define CSV file path for the final merged data
final_merged_csv_path = os.path.join(csv_dir, 'final_merged_data.csv')

# Write the final merged data to a CSV file
final_merged_df.to_csv(final_merged_csv_path, index=False)

print(f'Final merged data CSV file created at: {final_merged_csv_path}')

# Close the connection
conn.close()

