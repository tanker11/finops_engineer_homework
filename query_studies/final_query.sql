--Create a table with warehouse names, tasks, and calculated CPU cost, ranked by cpu_cost per warehouse partitions
--Table joined first with the CPU cost vaues via common instance_name value
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

