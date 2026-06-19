import pandas as pd
import numpy as np
import pgeocode


# Read the excel file into a pandas DataFrame
df = pd.read_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/FireDeptData.xlsx')

address = (
    df["Incident Full Address"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Extract Zipcode from the end of address
df["Zipcode"] = (
    address.str.extract(r"(\d{5})$")[0]
    .astype("string")
    .str.strip()
    .str.zfill(5)
)

# Use pgeocode to get city from ZIP code
nomi = pgeocode.Nominatim("us")
zip_info = nomi.query_postal_code(df["Zipcode"].tolist())

df["City"] = zip_info["place_name"].values
df["State"] = zip_info["state_code"].values

# Clean the formatting for  columns Zipcode, City, State
df["Zipcode"] = df["Zipcode"].astype("string")
df["City"] = df["City"].astype("string").str.title()
df["State"] = df["State"].astype("string").str.upper()


# Create Location Dimension table and making sure the main table will only have required columns 
location_dim = df[["Zipcode", "City", "State"]].copy()

# Remove blank or missing ZIP codes
location_dim = location_dim.dropna(subset=["Zipcode"])

# Remove duplicate locations
location_dim = location_dim.drop_duplicates()

# Sort by Zipcode
location_dim = location_dim.sort_values(by="Zipcode")

# Optional: create Location ID
location_dim.insert(0, "LocationID", range(1, len(location_dim) + 1))

# Save as a separate Excel file
location_dim.to_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Location_Dimension.xlsx", index=False)

# Reorder FireDept table columns
cols = [
    'Incident Number',
    'Incident Full Address',
    'Zipcode',
    'Primary Station',
    'Cold Response',
    'Incident Type Category',
    'Unit Call Sign',
    'PSAP DateTime',
    'Alarm DateTime',
    'Enroute DateTime',
    'Arrival DateTime'
]

df = df[cols]

# Store the FireDept table with the new columns and cleaned data
df.to_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/FireDept_table.xlsx', index=False, engine="openpyxl")