import sqlite3

# Connect to the database (creates it if it doesn't exist)
connection = sqlite3.connect('database.db')

# Open and read the schema.sql file
with open('schema.sql') as f:
    connection.executescript(f.read())

print("Database successfully built from schema.sql!")
connection.close()