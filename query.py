import sqlite3
import pandas as pd

# Paraméterek
db_name = "/app/loaddata.db"

# Lekérdezés, amely a top 3 legnagyobb költségű feladatot gyűjti ki raktáranként
query = """
WITH COST_RANK_CTE as
(
SELECT warehouse_name,
       task_name,
       cpu_ms*c.cpu_ms_cost as cpu_cost,
       ROW_NUMBER() OVER(PARTITION BY warehouse_name ORDER BY cpu_ms*c.cpu_ms_cost DESC) as rank_wh
  FROM metrics m
JOIN costs c
ON m.instance_name=c.instance_name
ORDER BY warehouse_name
),

--Create a table with warehouse names and tasks ranked by the instance count per this combination
USAGE_CTE as
(
SELECT warehouse_name,
       task_name,
       instance_name,
       COUNT(instance_name) as instance_count,
       ROW_NUMBER() OVER (PARTITION BY warehouse_name,task_name ORDER BY COUNT(instance_name) DESC) as usage_rank
  FROM metrics
  GROUP BY warehouse_name, task_name, instance_name
),

--Create a query that selects only those having rank=1 under the name USAGE_QUERY
USAGE_QUERY as
(
SELECT warehouse_name,
    task_name,
    instance_name,
    instance_count
FROM USAGE_CTE
WHERE usage_rank=1
ORDER BY warehouse_name, task_name

)

--Create a query that shows the TOP3 cost coming from warehouse_and_task combos, and join the USAGE_QUERY that shows the most used instance names and count of usages
SELECT r.warehouse_name, r.task_name,r.rank_wh,r.cpu_cost,u.instance_name,u.instance_count
FROM COST_RANK_CTE as r
JOIN USAGE_QUERY as u
  ON r.warehouse_name=u.warehouse_name AND r.task_name=u.task_name
WHERE rank_wh<4  
ORDER BY r.warehouse_name, rank_wh
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
    main()