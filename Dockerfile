FROM python:3.13-slim

# Mappa létrehozása és munka könyvtár beállítása
WORKDIR /app

# Függőségek telepítése
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Script-ek és adatok bemásolása
COPY *.py /app
COPY *.json /app

# A python fájlok futtatása egymás után
ENTRYPOINT ["sh", "-c"]
CMD ["python ddl.py && python etl.py && python query.py"]

