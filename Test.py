import pandas as pd
import psycopg2
from psycopg2 import sql

# Read CSV into pandas DataFrame
df = pd.read_excel('Data/testing01.xlsx')
df.columns = df.columns.str.lower().str.replace(' ', '_')
# Print the DataFrame to ensure it's loaded correctly
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

    # Check the contents of the average_rents table
    cursor.execute("SELECT * FROM average_rents;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("I'm in the database!")

    # Define the table name (ensure no extra space)
    table_name = "average_rents"

    # Get column names from DataFrame
    columns = df.columns.tolist()

    # Create dynamic query placeholders with properly quoted column names
    column_names = ', '.join([f'"{col}"' for col in columns])  # Quote column names
    placeholders = ', '.join(['%s'] * len(columns))

    # Insert data into the table row by row
    count = 0
    for index, row in df.iterrows():
        print(count)
        count += 1
        # Prepare the insert query
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(column_names),
            sql.SQL(placeholders)
        )
        
        # Convert row to tuple and execute the query
        cursor.execute(query, tuple(row))

    # Commit changes to the database
    connection.commit()
    print("Data inserted successfully!")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()

print("Hello World!")
