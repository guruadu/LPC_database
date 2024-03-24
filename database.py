import sqlite3
import pandas as pd

def get_all_addresses(db_file, table_name):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f"SELECT address FROM [{table_name}]")
        addresses = cursor.fetchall()
        addresses = [address[0] for address in addresses if address[0] is not None]
        return addresses
    except sqlite3.Error as e:
        print("Error fetching addresses:", e)
    finally:
        cursor.close()
        conn.close()

def excel_sheets_to_sqlite(excel_file, db_file):
    conn = sqlite3.connect(db_file)
    all_sheet_names = pd.ExcelFile(excel_file).sheet_names
    for sheet_name in all_sheet_names:
            try:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                df.to_sql(sheet_name, conn, index=False, if_exists='replace')
            except Exception as e:
                print(f"Error processing '{sheet_name}': {e}")
    
    conn.close()
    
def get_ngo_name(db_file, address, table_name):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f"SELECT `NGO Name`, `Phone No.`, `E-mail`, Address, Comments FROM [{table_name}] WHERE Address = ?", (address,))
        ngo_details = cursor.fetchall()
        return ngo_details
    except sqlite3.Error as e:
        print("Error fetching addresses:", e)
    finally:
        cursor.close()
        conn.close()
