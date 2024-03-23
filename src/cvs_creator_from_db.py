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

# Extract tables from metadata
tables = metadata.tables.keys()

# Create CSV directory if it doesn't exist
csv_dir = '/workspaces/Machine-Learning-Final-Project/data/csv'
os.makedirs(csv_dir, exist_ok=True)

# Loop through tables and create CSV files
for table_name in tables:
    # Load table
    table = Table(table_name, metadata, autoload=True, autoload_with=engine)
    
    # Create connection
    conn = engine.connect()
    
    # Check if the table is 'station'
    if table_name == 'station':
        # Define raw SQL query to select all columns and the count of stations grouped by state
        query = text(f"SELECT *, (SELECT COUNT(*) FROM {table_name} AS s WHERE s.state = {table_name}.state) AS number_of_stations FROM {table_name}")
    else:
        # Define raw SQL query to select all columns from the table
        query = text(f"SELECT * FROM {table_name}")
    
    result = conn.execute(query)
    
    # Fetch all rows into a DataFrame    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Define CSV file path
    csv_file_path = os.path.join(csv_dir, f'{table_name}.csv')
    
    # Write DataFrame to CSV
    df.to_csv(csv_file_path, index=False)
    
    print(f'CSV file created for table {table_name} at: {csv_file_path}')
    
    # Close connection
    conn.close()

print("CSV files created successfully!")



