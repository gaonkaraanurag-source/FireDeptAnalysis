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

# Extract City, State, and optional ZIP from the end
extracted = address.str.extract(
    r"(?P<City>[A-Za-z\s]+)\s+(?P<State>[A-Za-z]{2})(?:\s+(?P<Zipcode>\d{5}))?$"
)

df["City"] = extracted["City"].str.strip()
df["State"] = extracted["State"].str.upper()
df["Zipcode"] = extracted["Zipcode"]

# Clean the zip code by ensuring it's a string and removing any non-numeric characters
df["Zipcode"] = df["Zipcode"].astype(str).str.extract(r"(\d{5})")

# Use pgeocode to get city from ZIP code
nomi = pgeocode.Nominatim("us")
zip_info = nomi.query_postal_code(df["Zipcode"].tolist())
df["City"] = zip_info["place_name"].values

# Clean the formatting for State columns by converting them to uppercase and title case respectively
df['State'] = df['State'].str.upper()

# Delete the original Incident Full Address column as we have extracted the necessary information from it
#df.drop('Incident Full Address', axis=1, inplace=True)

# Reorder the columns to have Address, City, State, Zipcode at the beginning
cols = df.columns.tolist()
cols = ['Incident Number','Incident Full Address', 'City', 'State', 'Zipcode','Primary Station','Cold Response','Incident Type Category', 'Incident Type', 'Unit Call Sign','Alarm DateTime','Enroute DateTime','Arrival DateTime'] 
df = df[cols]
# Store the cleaned data in a new excel file
#df.to_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Updated_Fire_Dept_Data.xlsx', index=False, engine="openpyxl")

# Create Location Dimension table
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

