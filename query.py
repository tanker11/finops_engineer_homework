import sqlite3
import pandas as pd
import time

# Paraméterek
db_name = "/app/loaddata.db"

# Lekérdezés, amely a top 3 legnagyobb költségű feladatot gyűjti ki raktáranként
query = """
--Pre create a CTE calculating all the costs in advance by joining the costs table to metrics
WITH METRICS_WITH_COST AS (
  SELECT 
       m.warehouse_name,
       m.task_name,
       m.instance_name,
       m.cpu_ms * c.cpu_ms_cost AS cpu_cost
  FROM metrics m
  JOIN costs c
    ON m.instance_name = c.instance_name
),

--Create a CTE with warehouse names ranked by the descending cost
COST_RANK AS (
  SELECT 
       warehouse_name,
       task_name,
       cpu_cost,
       ROW_NUMBER() OVER (PARTITION BY warehouse_name ORDER BY cpu_cost DESC) AS rank_wh
  FROM METRICS_WITH_COST
),

--Create a CTE that shows the usage rank for the warehouse+task name combinations
USAGE_RANK AS (
  SELECT 
       warehouse_name,
       task_name,
       instance_name,
       COUNT(instance_name) AS instance_count,
       ROW_NUMBER() OVER (PARTITION BY warehouse_name, task_name ORDER BY COUNT(instance_name) DESC) AS usage_rank
  FROM metrics
  GROUP BY warehouse_name, task_name, instance_name
)

--Create a query that shows the TOP3 cost coming from warehouse_and_task combos, and join the USAGE_QUERY that shows the most used instance names and count of usages
SELECT 
       c.warehouse_name, 
       c.task_name,
       c.rank_wh,
       c.cpu_cost,
       u.instance_name,
       u.instance_count
FROM COST_RANK c
JOIN USAGE_RANK u
  ON c.warehouse_name = u.warehouse_name AND c.task_name = u.task_name
WHERE c.rank_wh < 4 AND u.usage_rank = 1
ORDER BY c.warehouse_name, c.rank_wh;


"""

def fetch_data_as_dataframe():
    # SQLite kapcsolat létrehozása
    conn = sqlite3.connect(db_name)
    try:
        # Adatok beolvasása Pandas DataFrame-be
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        # Kapcsolat bezárása
        conn.close()

def main():
    print("Started querying data from tables...")
    # Adatok lekérése Pandas DataFrame-be
    df = fetch_data_as_dataframe()

    # Top 3 feladat raktáranként
    top_3_by_warehouse = df.groupby("warehouse_name").head(3)
    
    # Adatok kiírása
    print("\nTop 3 tasks per warehouse that produced the highest costs along with the instances used by them the most:")
    print(top_3_by_warehouse)

if __name__ == "__main__":
    st = time.time()
    
    print("*"*20,"3 - QUERY FUTTATÁSA","*"*20)

    main()
    
    et = time.time()

    print(f'Execution time: {et-st:.3f} seconds')