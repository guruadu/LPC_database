import sqlite3

def get_all_addresses(db_file, table_name):
    try:
        # Create SQLite connection
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Execute SQL query to select all addresses from the table
        cursor.execute(f"SELECT address FROM {table_name}")
        
        # Fetch all addresses
        addresses = cursor.fetchall()

        if addresses:
            print("Addresses:")
            for address in addresses:
                print(address[0])
                print("\n")
        else:
            print("No addresses found in the table.")

    except sqlite3.Error as e:
        print("Error fetching addresses:", e)

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

# Example usage
db_file = 'data.db'  # Replace 'your_database.db' with the actual path to your SQLite database file
table_name = 'Delhi'  # Replace 'ngo_table' with the actual name of your table
get_all_addresses(db_file, table_name)
