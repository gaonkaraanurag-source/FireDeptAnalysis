# Create Date Dimension Table 
import pandas as pd

# Read the excel file
df = pd.read_excel('/Users/anuraggaonkar/Downloads/Data Analyst Assignment/FireDeptData.xlsx')
# Convert date columns to datetime
date_columns = ["PSAP DateTime", "Alarm DateTime", "Enroute DateTime", "Arrival DateTime"]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Find minimum and maximum date from all datetime columns
min_date = df[date_columns].min().min()
max_date = df[date_columns].max().max()

# Create date range
date_dim = pd.DataFrame({
    "Date": pd.date_range(start=min_date, end=max_date, freq="D")
})


# Create date attributes
date_dim["DateID"] = date_dim["Date"].dt.date
date_dim["Year"] = date_dim["Date"].dt.year
date_dim["Quarter"] = "Q" + date_dim["Date"].dt.quarter.astype(str)
date_dim["MonthNumber"] = date_dim["Date"].dt.month
date_dim["MonthName"] = date_dim["Date"].dt.month_name()
date_dim["MonthYear"] = date_dim["Date"].dt.strftime("%b %Y")
date_dim["Day"] = date_dim["Date"].dt.day
date_dim["DayName"] = date_dim["Date"].dt.day_name()
date_dim["DayOfWeek"] = date_dim["Date"].dt.dayofweek + 1
date_dim["WeekOfYear"] = date_dim["Date"].dt.isocalendar().week
date_dim["IsWeekend"] = date_dim["DayName"].isin(["Saturday", "Sunday"])

# Rearrange columns
date_dim = date_dim[
    [
        "DateID",
        "Date",
        "Year",
        "Quarter",
        "MonthNumber",
        "MonthName",
        "MonthYear",
        "Day",
        "DayName",
        "DayOfWeek",
        "WeekOfYear",
        "IsWeekend"
    ]
]

# Save as Excel
date_dim.to_excel("/Users/anuraggaonkar/Downloads/Data Analyst Assignment/Date_Dimension.xlsx", index=False)