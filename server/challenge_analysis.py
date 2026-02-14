import geopandas as gpd
from sqlalchemy import create_engine

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221"
user = "ajdcc"
password = "gme221_db"

# Create connection string
conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

# Create SQLAlchemy engine
engine = create_engine(conn_str)

# Minimal SQL queries (no spatial operations)
sql_parcel = "SELECT parcel_pin, geom FROM public.parcel"
sql_landuse = "SELECT name, geom FROM public.landuse"

# Loading data into GeoDataFrames
parcels = gpd.read_postgis(sql_parcel, engine, geom_col="geom")
landuse = gpd.read_postgis(sql_landuse, engine, geom_col="geom")

# Reproject to EPSG:3395 for area calculations
parcels = parcels.to_crs(epsg=3395)
landuse = landuse.to_crs(epsg=3395)

# Compute total area of parcel
parcels["total_area"] = parcels.geometry.area

# Perform spatial intersection
overlay = gpd.overlay(parcels, landuse, how="intersection")
overlay["landuse_area"] = overlay.geometry.area

# Compute area percentage within a land use category
overlay["percentage"] = (
    overlay["landuse_area"] / overlay["total_area"]
) * 100

overlay["percentage"] = overlay["percentage"].round(2)

# Identify the indexes of the parcels that have multiple land uses
mixed_parcels_idx = overlay.groupby("parcel_pin").filter(lambda x: len(x) > 1).index # len(x) > 1 means that a parcel_pin appears more than once in the overlay geodataframe

# Using the identified indices of the mixed_parcels, fetch all features matching the condition using the .loc method
mixed = overlay.loc[mixed_parcels_idx, ["parcel_pin", "name", "percentage"]]

# Identify the max percentage share of a land use of parcels
max_per_parcel = mixed.groupby("parcel_pin")["percentage"].max()

# Get parcel_pin values of parcels that have no single land use greater than 60%
mixed_use_parcel_pins = max_per_parcel[max_per_parcel <= 60].index

# Extract parcels with no single land use greater than 60% using the .isin() method
mixed_use_final = mixed[mixed["parcel_pin"].isin(mixed_use_parcel_pins)]

# print(mixed_use_final.head())

# Revert back to the original geometry
geom = overlay[["parcel_pin","geometry"]].dissolve(
    by="parcel_pin").reset_index()

# Merge using original geometry using the "right" join to only match those that are in the mixed_use_final df items
final_output = geom.merge(
    mixed_use_final,
    on="parcel_pin",
    how="right"
)

# Reprojecting it back to EPSG 4326
final_output = final_output.to_crs(epsg=4326)

# print(final_output.head())

# Exporting to a GeoJSON file for interpretation
final_output.to_file(
    "output/challenge_result.geojson",
    driver="GeoJSON"
)

print("GeoJSON saved successfully.")