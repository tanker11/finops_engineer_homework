import sqlite3

# Adatbázis és DDL paraméterek
db_name = "/app/loaddata.db"
ddl_list = [
    '''
    CREATE TABLE IF NOT EXISTS metrics (
        warehouse_name TEXT,
        task_name TEXT,
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
    ''',
    '''
    CREATE INDEX idx_metrics_warehouse_task_instance 
    ON metrics (warehouse_name, task_name, instance_name);
    ''',
    '''
    CREATE INDEX idx_costs_instance_name 
    ON costs (instance_name);
    '''

]

# Adatbázis inicializálása és táblák létrehozása
def init_db():
    print("Creating database file...")
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        for ddl_query in ddl_list:
            cursor.execute(ddl_query)
        conn.commit()
    print(f"Database '{db_name}' initialized and tables created.")

if __name__ == "__main__":
    init_db()
