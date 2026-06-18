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

# Lets clean the formatting for Incident Full Address columns by removing spaces and capitalizing the first letter of each word
#df['Incident Full Address'] = df['Incident Full Address'].str.strip().str.title()

# Extract 5-digit ZIP code only if it exists at the end of the address
#df["Zipcode"] = df["Incident Full Address"].str.extract(r"(\d{5})\s*$")

# Remove ZIP code before extracting state/city
#address_without_zip = df["Incident Full Address"].str.replace(r"\s+\d{5}\s*$", "", regex=True)

# Extract state only if it is a 2-letter state code at the end
#df["State"] = address_without_zip.str.extract(r"\s([A-Z]{2})\s*$")

# Remove state before extracting city
#address_without_state = address_without_zip.str.replace(r"\s+[A-Z]{2}\s*$", "", regex=True)

# Extract city as the last word before state
#df["City"] = address_without_state.str.split().str[-1]

# Lets get Zipcode, State and City from the Incident Full Address column and create new columns for them
#df['Zipcode'] = df['Incident Full Address'].str.split().str[-1]
#df['State'] = df['Incident Full Address'].str.split().str[-2]
#df['City'] = df['Incident Full Address'].str.split().str[-3]

# Keep the rest of the address in the new address column
#df['Address'] = df['Incident Full Address'].str.split().str[:-3].str.join(' ')


# Clean the formatting for State and City columns by converting them to uppercase and title case respectively
df['State'] = df['State'].str.upper()
df['City'] = df['City'].str.title()

# Delete the original Incident Full Address column as we have extracted the necessary information from it
#df.drop('Incident Full Address', axis=1, inplace=True)

# Reorder the columns to have Address, City, State, Zipcode at the beginning
cols = df.columns.tolist()
cols = ['Incident Number','Incident Full Address', 'City', 'State', 'Zipcode','Primary Station','Cold Response','Incident Type Category', 'Incident Type', 'Unit Call Sign','Alarm DateTime','Enroute DateTime','Arrival DateTime'] 
df = df[cols]
# Store the cleaned data in a new excel file
df.to_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Updated_Fire_Dept_Data.xlsx', index=False, engine="openpyxl")

#print(df.head())