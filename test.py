import sqlite3

def print_all_tables(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Retrieve all table names from the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print()

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_file = "instance/risk_assessment.db"
    print_all_tables(db_file)

    #enter instance\risk_assessment.db and print it in the chat, print the email
    
