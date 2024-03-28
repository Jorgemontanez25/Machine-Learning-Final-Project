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

# Create a connection
conn = engine.connect()

# Define SQL query to group station data by state and calculate aggregated values
query = text("""
    SELECT 
        state_ab, 
        IFNULL(SUM(CAST("ev_level1_evse_num" AS INT)), 0) as "Total_EV_Level1_EVSE_Num", 
        IFNULL(SUM(CAST("ev_level2_evse_num" AS INT)), 0) as "Total_EV_Level2_EVSE_Num", 
        IFNULL(SUM(CAST("ev_dc_fast_count" AS INT)), 0) as "Total_EV_DC_Fast_Count", 
                COUNT(DISTINCT(id)) as "stations_number"
    FROM 
        station 
    GROUP BY 
        state_ab
""")

# Execute the query
result = conn.execute(query)

# Fetch the results into a DataFrame
station_df = pd.DataFrame(result.fetchall(), columns=result.keys())

# Define CSV file path for the station data
station_csv_path = os.path.join(csv_dir, 'station.csv')

# Write the station data to a CSV file
station_df.to_csv(station_csv_path, index=False)

# Close the connection
conn.close()

print(f'Station data CSV file created at: {station_csv_path}')
