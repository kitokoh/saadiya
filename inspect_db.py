import sqlite3

def inspect_database(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"Tables in {db_file}:")
        for table_name in tables:
            print(f"\nTable: {table_name[0]}")

            # Get the table schema
            cursor.execute(f"PRAGMA table_info({table_name[0]});")
            columns = cursor.fetchall()

            print("Columns:")
            for column in columns:
                print(f"  - {column[1]} ({column[2]})")

        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    inspect_database("nova360.db")
