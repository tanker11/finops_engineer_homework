import sqlite3
import pandas as pd
import json
import os

# Paraméterek
db_name = "loaddata.db"
json_list = ["metrics.json", "costs.json"]

# JSON fájl beolvasása és táblázatos formátumra alakítása
def load_json(json_file):
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file not found: {json_file}")
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        # A metrics.json szabályos, azt dataframe-mé alakítjuk, míg a costs.json nem ilyen, így hiányoznak a mezőnevek, ezt pótoljuk
        return pd.DataFrame([{"instance_name": k, "cpu_ms": v} for k, v in data.items()])
        # Átalakítjuk a szótárat egy listává, sajnos ez hard wired, mert nincsenek oszlopneveink
    else:
        return pd.DataFrame(data)

# Adatok írása az adatbázisba
def write_to_db(table_name, df):
    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f'{len(df)} rows stored in the table {table_name}')

# JSON fájlok feldolgozása
def process_json_files():
    for json_file in json_list:
        # JSON beolvasása
        df = load_json(json_file)
        print(f"Data from {json_file}:")
        print(df)

        # Táblanév a JSON fájl nevéből
        table_name = json_file.split(".")[0]

        # Adatok írása az adatbázisba
        write_to_db(table_name, df)


if __name__ == "__main__":
    process_json_files()
