FROM python:3.11

EXPOSE 5000

WORKDIR /app

ENV FLASK_APP=app.py

COPY requirements.txt .

# Install GDAL dependencies for geopandas' dependency (fiona)
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]    