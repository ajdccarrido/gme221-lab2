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

### D.2 Reflection - Spatial Process and Classification
1. *Why is CRS transformation necessary before area computation?*
- CRS transformation converts geographic units (degrees) into linear units (sq.m, ha, acres, etc.) which represents area computations more accurately.

2. *How does CRS choice affect area accuracy?*
- CRS choice affects area accuracy significantly. A projected coordinate reference system should always be used whenever area computations are implemented so that area computations are accurate. 

3. *Does the overlay create new spatial units that did not previously exist?*
- Yes. It creates new features based on the intersection of the parcels and landuse GeoDataFrames

4. *Why is classification considered part of the analysis process?*
- We are now working on new derived data based on the steps implemented. We also filtered and queried the attributes of the created data to operationalize spatial operations and answer spatial queries.


5. *Is classification sensitive to sliver geometries or topology errors?"
- I believe not. Because the classification we implemented are already attribute-based. Spatial operations, on the other hand, are sensitive to sliver geometries and topology errors.

6. *Would changing the dominance threshold alter spatial patterns?*
- Yes. Increasing or decreasing the thresholds (even just by 1%) WILL ALTER spatial patterns since we are implementing the filter based on computed field values.

### E.3 Reflection - Visualization and Interpretation in QGIS
- To visualize the results, I used Natural Jenks as the symbology, with the red areas representing high residential land use dominance. Most of the parcels (280 out of 15) had 100% of their total land area belonging to the residential land use, with the exception of some parcels and the road lots the also overlapped with other land use categories. Some parcels located in the lower part had approximately 75% of their land area belonging to land use, with the remaining fraction belonging to other categories.

### Part F. Challenge Exercise - Design Your own Spatial Analysis
1. *What spatial question did you choose?*
- I chose Option 2 - Identify all Mixed-Use Parcels. The condition set is that there should be no single land use that must exceed by 60%

2. *What algorithmic steps did you design?*
#### STEP 1. AREA COMPUTATIONS
I followed the steps from the previous part up to the computation the percentage of land use relative to the total area of a parcel.

#### STEP 2. IDENTIFY PARCELS WITH MORE THAN ONE LAND USE CATEGORY

#### STEP 3. APPLY CONDITIONAL FILTERING

#### STEP 4. MERGE ORIGINAL GEOMETRY WITH THE RESULTING GEODATAFRAME

#### STEP 5. EXPORT RESULTS AND INTERPRET IN QGIS