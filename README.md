# Eredeti kiírás

Honky-tonk Fruits Co. spent a huge load of money on migrating to a cloud provider with bad reputation, and now the CTO realizes that they will go bankrupt in a year with the current costs of cloud computing. 
They need very quick analytics on some dumped data. “metrics.json” contains some metrics of the executed jobs, “costs.json” provide you the unit costs (cost / cpu_ms).
Your task is to provide code for:
1.	Local database deployment (Dockerfile). You are free to choose the database.
2.	DDL for the schema you designed for the reporting (ddl.sql or ddl.py)
3.	Data loader (etl.py)
4.	Write query: which are the top3 tasks per warehouse that produced the highest costs and which instances were used by these tasks mostly (query.py or query.sql)


# Megoldás

## Adatbázis
SQLite adatbázismotort választottam, a megoldások Python kódban vannak elkészítve.

## Analízis
A rendelkezésre bocsátott adatok közül a metrics.json file teljes JSON formátumú, míg a costs.json egy python dict.
Így az adatok beolvasásakor ezt figyelembe véve az importáláshoz további lépéseket adtam, és a metrics.json logikájához illeszkedően neveztem el a mezőket.

## DDL.py
A kód létrehoz egy üres adatbázist /app/loaddata.db néven.
DDL query kód(ok) futtatásával létrehoz egy metrics és egy costs táblát, a JSON inputnak megfelelő mezőkkel, és úgy, hogy feltételezzük, hogy az instance_name mező lesz az a kulcs a costs táblában, ami alapján összekapcsoljuk a két táblát.
Valamint létrehoz egy indexet is a metrics táblához a leggyakrabban használt mezőkön, melyeket JOIN vagy GROUP BY esetén használunk.

## ETL.py
Ez a kód az adatok betöltését és adatbázisba írását végzi. Figyel arra, hogy a cost.json file nem teljes JSON.
Az előző kódban létrehozott táblákba tölti az adatokat úgy, hogy Pandas DataFrame-be tölti, majd Pandas to_sql metódussal kiírja.

## QUERY.py
Lefuttat egy összetett lekérdezést a kiírásnak megfelelő válasz létrehozása érdekében.

### A query értelmezése
A részeredmények, illetve válaszok a /query_studies illetve annak /pictures almappájában vannak, ezen vizsgálatokból és részeredményekből épül össze a teljes megoldás.

A végső megoldásban a következők történnek:
1. Összekapcsoljuk a metrics és a costs táblákat, és kiszámítjuk a cpu_cost értékét a cpu_ms és a cpu_ms_cost szorzataként minden elemre, és eltesszük egy CTE-be (METRICS_WITH_COST)
2. Létrehozunk egy COST_RANK nevű CTE-t, amelyben a warehouse_name szerinti particionálással csökkenő sorrendet alakítunk ki az előző CTE-n alapuló lekérdezéssel, a cpu_cost alapján.
3. Létrehozunk egy USAGE_RANK CTE-t, amiben sorrendet állapítunk meg az alapján, hogy melyik warehouse_name+task_name kombináció használja a legtöbb instance-et.
4. Ebben a lépésben a COST_RANK és USAGE_RANK CTE-ket JOIN-nal összekötjük a warehouse_name+task_name alapján, és megjelenítjük azokat, amelyek 4-nél kisebb (TOP 3) rangsorúak a COST, valamint első helyen vannak a USAGE alapján.
A kimenet tartalmazza a raktár nevét, a task nevét (minden raktárhoz 3 taskot, amelyek a legtöbbe kerülnek), a rank értékét, a költésget, valamint a warehouse_name+task_name kombináció alapján kikeresett instance neveket valamint a darabszámot, ahányszor ez a kombináció használja az instance_et.
Megjegyzés: előfordulhat, hogy az adott raktár esetében többször is előfordul ugyanaz a task_name, így az ehhez a kombinációhoz kikeresett legtöbb instance használat is értelemszerűen ugyanaz ilyenkor.

## Konténerizálás
Az elkészült kódokat egy Python alapú konténerben futtatjuk, a Dockerfile nevű állományban meghatározottak alapján:
- létrejön egy Python konténer egy slim Python image alapján
- kijelöljük a munkamappát (/app)
- a requirements.txt fájlban felsoroljuk a python könyvtárakat, melyeket telepíteni kell a sikeres futtatáshoz
- felmásoljuk a python és json állományokat a munkamappába
- a ddl.py, etl.py és query.py kódokat egymás után futtatjuk
- az eredmények a konzolon jelennek meg

### A konténer megoldás használata:

Szükség van egy telepített Docker Desktop alkalmazásra, majd ezután:

Konténer felépítése:
 '''docker build -t finopshomework .'''

Konténer futtatása:
 '''docker run --rm finopshomework'''