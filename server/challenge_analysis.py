import geopandas as gpd
from sqlalchemy import create_engine

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221"
user = "postgres"
password = "Elupdb2025*"

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
mixed_parcels_idx = overlay.groupby("parcel_pin").filter(lambda x: len(x) > 1).index # len(x) > 1 means that all parcel_pin appearing more than once in the overlay geodataframe

# Using the identified indices of the mixed_parcels, fetch all features matching the condition using the .loc method
mixed = overlay.loc[mixed_parcels_idx, ["parcel_pin", "name", "percentage", "geometry"]]

# Identify all parcels that have a land use greater than 60
non_mixed_use_idx = mixed.groupby("parcel_pin")["percentage"].max().loc[lambda x: x > 60].index

# Get all parcels with no land use greater than 60 using the tilde operator (inverse)
mixed_use_parcels = mixed[~mixed["parcel_pin"].isin(non_mixed_use_idx)]

geom = overlay[["parcel_pin","geometry"]].dissolve(
    by="parcel_pin").reset_index()

final_mixed_use = geom.merge(
    mixed_use_parcels,
    on="parcel_pin",
    how="left"
)

# Reprojecting it back to EPSG 4326
final_mixed_use = final_mixed_use.to_crs(epsg=4326)

# Exporting to a GeoJSON file for interpretation
final_mixed_use.to_file(
    "output/challenge_result2.geojson",
    driver="GeoJSON"
)