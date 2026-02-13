# GmE 221 – Laboratory Exercise 2

## Overview 
This laboratory performs a parcel–landuse overlay analysis using Python (GeoPandas). 
Spatial data are retrieved from PostGIS using minimal SQL.   
Overlay, area computation, percentage calculation, and classification are executed in Python. 
The final output is exported as a GeoJSON file for visualization in QGIS. 

--- 

## Environment Setup 
- Python 3.x 
- PostgreSQL with PostGIS 
- GeoPandas, SQLAlchemy, psycopg2 

--- 

## How to Run 
1. Activate the virtual environment 
2. Run `analysis.py` to execute the overlay and classification 
3. Load the generated GeoJSON file in QGIS 

--- 

## Outputs 
- GeoJSON file: `output/dominant_residential.geojson` 
- Visualization in QGIS 

## Reflection
### B.6 Reflection Questions
1. *What is the difference between storing geometry in PostGIS and representing it in GeoPandas?*
- The difference in storing geometry in PostGIS vs in GeoPandas is that the geometry format in PostGIS is in Well-Known Binary (WKB) format while GeoPandas represent it in Well-Known Text (WKT)

2. *Why is this step considered Input (IO) rather than analysis?*
- This step is only considered as input as the data is only fetched from the database source and transformed into another machine-readable form in preparation for the analysis.

3. *How does this relate to the "Input / Process / Output" structure of GIS algorithms discussed in Lecture 3?*
- This procedure is a prerequisite of any geoprocessing. This establishes that any data to be processed is compatible and can interact with each other.