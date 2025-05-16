import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/risk_assessment.db')
cursor = conn.cursor()

# Query to fetch the names of all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print each table name
print("Tables in the database:")
for table in tables:
    print(table[0])

cursor.execute("SELECT * FROM user")
users = cursor.fetchall()

print("\nRows in 'user' table:")
for user in users:
    print(user)

# Close the connection
conn.close()