#Category Dimension Table 
import pandas as pd

# Read the excel file 
df = pd.read_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/FireDeptData.xlsx')

# Select the required columns for the Category Dimension Table
category_dim = (
    df[["Incident Type Category", "Incident Type"]]
    .dropna(subset=["Incident Type Category", "Incident Type"], how="all")
    .drop_duplicates()
    .sort_values(["Incident Type Category", "Incident Type"])
    .reset_index(drop=True)
)


# Remove rows where both fields are blank
#category_dim = category_dim.dropna(
#   subset=["Incident Type Category", "Incident Type"],
#    how="all"
#)

# Create Category ID
category_dim.insert(0, "Category_ID", range(1, len(category_dim) + 1))

# Save to Excel
category_dim.to_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Category_Dimension1.xlsx", index=False)

