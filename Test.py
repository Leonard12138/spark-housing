import pandas as pd
import psycopg2
from psycopg2 import sql

# Load the Excel file
file_path = 'Data/testing01.xlsx'
df = pd.read_excel(file_path)

# Clean and format column names
df.columns = (
    df.columns
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('-', '', regex=False)
    .str.replace('_+', '_', regex=True)
)

# Clean numeric columns: Replace '-' and 'NaN' with None
numeric_columns = [
    col for col in df.columns if df[col].dtype in ['float64', 'int64'] or 'remarks' not in col
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, invalid values become NaN

# Print cleaned DataFrame
print("Cleaned DataFrame:")
print(df)

# Database connection setup
try:
    connection = psycopg2.connect(
        host="localhost",
        database="Testing1",
        user="postgres",
        password="123456",
        port=5432
    )
    cursor = connection.cursor()

    # Define the table name
    table_name = "average_rents"

    # Get column names from DataFrame
    columns = df.columns.tolist()

    # Create dynamic query placeholders
    column_names = ', '.join([f'"{col}"' for col in columns])
    placeholders = ', '.join(['%s'] * len(columns))

    # Insert data into the table
    for index, row in df.iterrows():
        # Prepare the insert query
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(column_names),
            sql.SQL(placeholders)
        )
        # Execute the query with row values
        cursor.execute(query, tuple(row))

    # Commit changes
    connection.commit()
    print("Data inserted successfully!")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close connections
    if cursor:
        cursor.close()
    if connection:
        connection.close()
