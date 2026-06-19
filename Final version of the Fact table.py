# Final version of the Fact table 
import pandas as pd
import numpy as np

# Read the excel file
df = pd.read_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Fact_FireDeptData1.xlsx')

print(df.shape)
print(df.columns)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()
print(df.columns)

# Removeing duplicate rows from the fact table
before_rows = len(df)
df = df.drop_duplicates()
after_rows = len(df)
print("Duplicate rows removed:", before_rows - after_rows)

#Convert Date/Time columns to datetime format
datetime_cols = [
    "PSAP DateTime",
    "Alarm DateTime",
    "Enroute DateTime",
    "Arrival DateTime"
]

for col in datetime_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

print(df[datetime_cols].dtypes)

# Lets make sure that the incident number year matches with the year in PSAP DateTime
# Extract year from PSAP DateTime
df["Incident Year"] = df["PSAP DateTime"].dt.year
print(df["Incident Year"].value_counts(dropna=False).sort_index())

# Removing rows with missing incident numbers 
before_rows = len(df)
df = df.dropna(subset=["Incident No Actual"])
after_rows = len(df)
print("Rows removed because Incident No Actual was missing:", before_rows - after_rows)

# Replace null values form the dimension files with 'None' 
text_cols = [
    "Incident No Actual",
    "Incident Full Address",
    "Primary Station",
    "Cold Response",
#    "Incident Type Category",
    "Unit Call Sign"
]

#New code added 
# Convert Category_ID to numeric format
df["Category_ID"] = pd.to_numeric(df["Category_ID"], errors="coerce").astype("Int64")


for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace(["nan", "None", ""], np.nan)

print(df[text_cols].head())

# Lets create response time metrics 
# Call Processing Time: Time from PSAP DateTime to Alarm DateTime
df["Alarm Handling Time"] = (
    df["Alarm DateTime"] - df["PSAP DateTime"]
).dt.total_seconds() / 60

# Turnout Time: Time from Alarm DateTime to Enroute DateTime
df["Turnout Time"] = (
    df["Enroute DateTime"] - df["Alarm DateTime"]
).dt.total_seconds() / 60

# Travel Time: Time from Enroute DateTime to Arrival DateTime
df["Travel Time"] = (
    df["Arrival DateTime"] - df["Enroute DateTime"]
).dt.total_seconds() / 60

# Total Response Time: Time from PSAP DateTime to Arrival DateTime
df["Total Response Time"] = (
    df["Arrival DateTime"] - df["PSAP DateTime"]
).dt.total_seconds() / 60

print(df[
    [
        "Alarm Handling Time",
        "Turnout Time",
        "Travel Time",
        "Total Response Time"
    ]
].describe())

# Let flag rows with missing or negative response times for review
df["Bad Response Time Flag"] = False

df.loc[
    (df["Alarm Handling Time"] < 0) |
    (df["Turnout Time"] < 0) |
    (df["Travel Time"] < 0) |
    (df["Total Response Time"] < 0),
    "Bad Response Time Flag"
] = True

print(df["Bad Response Time Flag"].value_counts())

# Flag missing response-time rows
df["Missing Response Time Flag"] = False

df.loc[
    df["PSAP DateTime"].isna() |
    df["Alarm DateTime"].isna() |
    df["Enroute DateTime"].isna() |
    df["Arrival DateTime"].isna(),
    "Missing Response Time Flag"
] = True

print(df["Missing Response Time Flag"].value_counts())

# Lets remove rows which will break response time analysis
fact_clean = df[
    (df["Bad Response Time Flag"] == False) &
    (df["Missing Response Time Flag"] == False)
].copy()

print("Original rows:", len(df))
print("Clean response-time rows:", len(fact_clean))

# Review the rejected rows to see if there are any patterns or if we can fix any of the issues
fact_rejected = df[
    (df["Bad Response Time Flag"] == True) |
    (df["Missing Response Time Flag"] == True)
].copy()

print("Rejected rows:", len(fact_rejected))

# Rearrange columns in the fact table
final_cols = [
    "Incident Year",
    "Incident No Actual",
    "Incident Full Address",
    "Zipcode",
    "Primary Station",
    "Cold Response",
 #   "Incident Type Category",
    "Category_ID",
    "Unit Call Sign",
    "PSAP DateTime",
    "Alarm DateTime",
    "Enroute DateTime",
    "Arrival DateTime",
    "Alarm Handling Time",
    "Turnout Time",
    "Travel Time",
    "Total Response Time",
    "Bad Response Time Flag"
]

facttable_FireDept = fact_clean[final_cols]
fact_rejected = fact_rejected[final_cols]

#Save the clean fact table and the rejected rows to separate Excel files for further analysis
facttable_FireDept.to_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Fact_FireDeptData_Cleaned1.xlsx", index=False)
fact_rejected.to_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Fact_FireDeptData_RejectedRows1.xlsx", index=False)

print("Files created successfully")
