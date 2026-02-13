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
- CRS choice affects area accuracy significantly. A projected coordinate reference system should always be used whenever area computations are implemented so that area computations are accurate. It is also vital to ensure that when working with multiple datasets, all must be in the same CRS.

3. *Does the overlay create new spatial units that did not previously exist?*
- Yes. It creates new features based on the intersection of the parcels and landuse GeoDataFrames

4. *Why is classification considered part of the analysis process?*
- We are now working on new derived data based on the steps implemented. We also filtered and queried the attributes of the created data to operationalize spatial operations and answer spatial queries.


5. *Is classification sensitive to sliver geometries or topology errors?"
- I believe not. Because the classification we implemented is already attribute-based. Spatial operations, on the other hand, are sensitive to sliver geometries and topology errors like the .overlay() function.

6. *Would changing the dominance threshold alter spatial patterns?*
- Yes. Increasing or decreasing the thresholds (even just by 1%) WILL ALTER spatial patterns since we are implementing the filter based on computed field values.

### E.3 Reflection - Visualization and Interpretation in QGIS
- To visualize the results, I used Natural Jenks as the symbology, with the red areas representing high residential land use dominance. Most of the parcels (280 out of 315) had 100% of their total land area belonging to the residential land use, with the exception of some parcels and the road lots the also overlapped with other land use categories. Some parcels located in the lower part had approximately 75% of their land area belonging to land use, with their remaining areas belonging to other categories.

### Part F. Challenge Exercise - Design Your Own Spatial Analysis

#### 1. *What spatial question did you choose?*
I chose Option 2 - Identify all Mixed-Use Parcels. The condition set is that there should be no single land use that must exceed by 60%

#### 2. *What algorithmic steps did you design?*
##### STEP 1. AREA COMPUTATIONS
I followed the steps from the previous part up to the computation of the percentage of a land use category relative to the total area of a parcel.

##### STEP 2. IDENTIFY PARCELS WITH MORE THAN ONE LAND USE CATEGORY
Firstly, I needed to know which parcel overlaps with multiple land use categories. To operationalize this, I used the .groupby() and .filter() methods to extract the index values of parcels. What this does is that it detects whether a parcel_pin appears multiple times in the ***overlay*** intersection layer. If it does, then those parcels overlap with multiple land uses. 

```bash
mixed_parcels_idx = overlay.groupby("parcel_pin").filter(lambda x: len(x) > 1).index
mixed = overlay.loc[mixed_parcels_idx, ["parcel_pin", "name", "percentage"]] 
```

The ***mixed*** variable now contains all the parcels that overlaps with multiple land uses.

##### STEP 3. APPLY CONDITIONAL FILTERING
I utilized the .groupby() and .max() operators to determine the maximum percentage share of various land uses on the parcels. Then, I used conditional filtering to select all maximum percentage shares that are less than 60% to satisfy the mixed use condition. I extracted the parcel_pin values of those features by using the .index attribute.

```bash
# Identify all parcel_pin values that have a land use greater than 60%
max_per_parcel = mixed.groupby("parcel_pin")["percentage"].max()

# Get parcel_pin values of parcels that have no single land use greater than 60%
mixed_use_parcel_pins = max_per_parcel[max_per_parcel <= 60].index
```

Now that I had identified the parcel_pin values of parcels that does not exceed the 60% threshold for any land use, I used the .isin() method to extract them from the original ***mixed*** GeoDataFrame.

```bash
# Extract parcels with no single land use greater than 60% using the .isin() method
mixed_use_final = mixed[mixed["parcel_pin"].isin(mixed_use_parcel_pins)]
```

##### STEP 4. MERGE ORIGINAL GEOMETRY WITH THE RESULTING GEODATAFRAME
The ***mixed_use_final*** output does not yet have a geometry, but it contains the required attribute to extract the original parcel geometry from the original ***overlay*** variable. I needed the parcel_pin to serve as my reference field so that I can connect the original geometry to the new dataframe using the .merge() method. This is similar to the JOIN operators in PostgreSQL.

##### STEP 5. EXPORT RESULTS AND INTERPRET IN QGIS

I exported the final GeoDataFrame to a GeoJSON file using the .to_file() method.

Most of the resulting parcels were road lots situated in Commercial and Residential Zones:
> - 193-01-0016-002-04
> - 193-01-0016-005-26
> - 193-01-0016-012-08
> - 193-01-0016-012-08
> - 193-01-0016-013-49

While one parcel (193-01-0016-016-51) was a property also situated in both Commercial and Residential Zones.

#### 3. *How does your logic differ from the guided example?*
In a high-level lens, my logic still follows the well-established convention of Input -> Process -> Output workflow. I just utilized other methods from the GeoPandas library to answer the spatial question at hand such as using the .isin(), .max(), and right join methods. 