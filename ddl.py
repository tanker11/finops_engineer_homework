import sqlite3

# Adatbázis és DDL paraméterek
db_name = "loaddata.db"
ddl_list = [
    '''
    CREATE TABLE IF NOT EXISTS metrics (
        warehouse_name TEXT,
        task_name_alma TEXT,
        instance_name TEXT,
        cpu_ms INTEGER,
        FOREIGN KEY (instance_name) REFERENCES costs(instance_name)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS costs (
        instance_name TEXT PRIMARY KEY,
        cpu_ms INTEGER
    );
    '''
]

# Adatbázis inicializálása és táblák létrehozása
def init_db():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        for ddl_query in ddl_list:
            cursor.execute(ddl_query)
        conn.commit()
    print(f"Database '{db_name}' initialized and tables created.")

if __name__ == "__main__":
    init_db()
