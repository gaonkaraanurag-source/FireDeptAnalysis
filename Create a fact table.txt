# Create a fact table 
import pandas as pd

# Read the excel file
df = pd.read_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/FireDept_table.xlsx")

# Read Category Dimension
category_dim = pd.read_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Category_Dimension1.xlsx")

# fact table will consist of following columns:
fact_table = [ 
    "Incident Number",
    "Incident Full Address",
    "Zipcode",
    "Primary Station",
    "Cold Response",
    "Incident Type Category",
    "Incident Type",
    "Unit Call Sign",
    "PSAP DateTime",
    "Alarm DateTime",
    "Enroute DateTime",
    "Arrival DateTime" 
]

fact_df = df[fact_table].copy()

# Remove rows where Incident Number is null
fact_df = fact_df.dropna(subset=["Incident Number"])

# Clean Incident Number format
fact_df["Incident Number Clean"] = (
    fact_df["Incident Number"]
    .astype("string")
    .str.strip()
    .str.replace("–", "-", regex=False)
    .str.replace("—", "-", regex=False)
    .str.replace("_", "-", regex=False)
    .str.replace("/", "-", regex=False)
    .str.replace(r"\s*-\s*", "-", regex=True)
)

# Split Incident Number into Year and Actual Incident Number
split_incident = fact_df["Incident Number Clean"].str.split("-", n=1, expand=True)

fact_df["Incident Year"] = split_incident[0]
fact_df["Incident No Actual"] = split_incident[1]

# Convert 2-digit year to 4-digit year
fact_df["Incident Year"] = fact_df["Incident Year"].apply(
    lambda x: "20" + x if pd.notna(x) and len(str(x)) == 2 else x
)

# Convert Incident Year to numeric
fact_df["Incident Year"] = pd.to_numeric(
    fact_df["Incident Year"], 
    errors="coerce"
).astype("Int64")

# Convert date columns to datetime format
datetime_cols = [
    "PSAP DateTime",
    "Alarm DateTime",
    "Enroute DateTime",
    "Arrival DateTime"
]

for col in datetime_cols:
    fact_df[col] = pd.to_datetime(fact_df[col], errors="coerce")

# Updating date field to match with the date dimension table
fact_df["PSAP_DateID"] = fact_df["PSAP DateTime"].dt.date
fact_df["Alarm_DateID"] = fact_df["Alarm DateTime"].dt.date
fact_df["Enroute_DateID"] = fact_df["Enroute DateTime"].dt.date
fact_df["Arrival_DateID"] = fact_df["Arrival DateTime"].dt.date


# Updating the Category fields to match with the category dimension table for merging
# Clean category merge fields in fact table
fact_df["Incident Type Category"] = (
    fact_df["Incident Type Category"]
    .astype("string")
    .str.strip()
    .str.replace(r"^\d+\s*-\s*", "", regex=True)
)

fact_df["Incident Type"] = (
    fact_df["Incident Type"]
    .astype("string")
    .str.strip()
)

# Clean category merge fields in category dimension
category_dim["Incident Type Category"] = (
    category_dim["Incident Type Category"]
    .astype("string")
    .str.strip()
    .str.replace(r"^\d+\s*-\s*", "", regex=True)
)

category_dim["Incident Type"] = (
    category_dim["Incident Type"]
    .astype("string")
    .str.strip()
)


# Bring Category_ID into fact table
fact_df = fact_df.merge(
    category_dim,
    on=["Incident Type Category", "Incident Type"],
    how="left"
)


# Remove original Incident Number and category text fields from fact table
fact_df = fact_df.drop(
    columns=[
        "Incident Number",
        "Incident Number Clean",
        "Incident Type Category",
        "Incident Type"
    ]
)

# Reorder Fact table columns
cols = [
     'Incident Year',
    'Incident No Actual',
    'Incident Full Address',
    'Zipcode',
    'Primary Station',
    'Cold Response',
    'Category_ID',
    'Unit Call Sign',

    # Date Dimension Keys
    'PSAP_DateID',
    'Alarm_DateID',
    'Enroute_DateID',
    'Arrival_DateID',

    # Original DateTime fields
    'PSAP DateTime',
    'Alarm DateTime',
    'Enroute DateTime',
    'Arrival DateTime'
]

fact_df = fact_df[cols]


# Save fact table
fact_df.to_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Fact_FireDeptData1.xlsx", index=False)