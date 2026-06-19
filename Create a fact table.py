# Create a fact table 
import pandas as pd

# Read the excel file
df = pd.read_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/FireDeptData.xlsx')

# fact table will consist of following columns:
fact_table = [ 
    "Incident Number",
    "Incident Full Address",
    "Incident Zip",
    "Primary Station",
    "Cold Response",
    "Incident Type Category",
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
    .str.replace("–", "-", regex=False)   # en dash
    .str.replace("—", "-", regex=False)   # em dash
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

# Optional: convert Incident Year to numeric
fact_df["Incident Year"] = pd.to_numeric(fact_df["Incident Year"], errors="coerce").astype("Int64")

# Save fact table
fact_df.to_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Fact_FireDeptData.xlsx", index=False)