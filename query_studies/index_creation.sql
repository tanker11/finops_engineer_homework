CREATE INDEX idx_metrics_warehouse_task_instance 
ON metrics (warehouse_name, task_name, instance_name);

--Nem szükséges, mert a cocts tábla kicsi
CREATE INDEX idx_costs_instance_name 
ON costs (instance_name);
