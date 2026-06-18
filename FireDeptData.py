import pandas as pd
import pgeocode

# Define the path to the excel file 
#file_path = 'Fire_Department_Data.xlsx'

# Read the excel file into a pandas DataFrame
df = pd.read_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/FireDeptData.xlsx')

# Display the first few rows of the DataFrame
#print(df.head())

# Lets clean the formatting for Incident Full Address columns by removing spaces and capitalizing the first letter of each word
df['Incident Full Address'] = df['Incident Full Address'].str.strip().str.title()

# Lets get Zipcode, State and City from the Incident Full Address column and create new columns for them
df['Zipcode'] = df['Incident Full Address'].str.split().str[-1]
df['State'] = df['Incident Full Address'].str.split().str[-2]
df['City'] = df['Incident Full Address'].str.split().str[-3]

# Keep the rest of the address in the new address column
df['Address'] = df['Incident Full Address'].str.split().str[:-3].str.join(' ')


# Clean the formatting for State and City columns by converting them to uppercase and title case respectively
df['State'] = df['State'].str.upper()
df['City'] = df['City'].str.title()

# Delete the original Incident Full Address column as we have extracted the necessary information from it
df.drop('Incident Full Address', axis=1, inplace=True)

# Reorder the columns to have Address, City, State, Zipcode at the beginning
cols = df.columns.tolist()
cols = ['Incident Number','Address', 'City', 'State', 'Zipcode','Primary Station','Cold Response','Incident Type Category', 'Incident Type', 'Unit Call Sign','Alarm DateTime','Enroute DateTime','Arrival DateTime'] 
df = df[cols]
# Store the cleaned data in a new excel file
df.to_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Updated_Fire_Dept_Data.xlsx', index=False, engine="openpyxl")

#print(df.head())