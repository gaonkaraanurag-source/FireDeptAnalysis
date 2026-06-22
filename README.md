# Fire Department Incident Analysis Dashboard

## Project Overview

This project analyzes Fire Department incident data using Python for data preparation and Tableau for dashboard reporting. The goal of this project is to help stakeholders understand incident volume, response time performance, station workload, city-level incident demand, and incident trends by month, hour, and day of week.

The final Tableau dashboard contains four main views:

1. **Summary**
2. **Station and Response Performance**
3. **Incident Volume Trends**
4. **Details Table**

---

## Business Objective

The dashboard was created to answer key operational questions such as:

- How many incidents occurred during the selected time period?
- What are the average alarm handling, turnout, travel, and total response times?
- Which cities have the highest number of incidents?
- Which incident categories occur most frequently?
- Where are incidents geographically concentrated?
- Which stations have the highest number of available units?
- Which stations and cities have higher average response times?
- What hours and weekdays have the highest incident volume?
- What percentage of incidents were cold response calls?

---

## Tools Used

- **Python**: Data cleaning, transformation, fact table creation, and dimension table creation
- **Pandas**: Data manipulation and calculations
- **Tableau**: Dashboard development and visualization
- **Excel**: Source and cleaned data storage
- **GitHub**: Version control and project documentation

---

## Dashboard Pages

### 1. Summary

The Summary page provides a high-level overview of fire department incidents.

It includes:

- Total Incidents
- Average Alarm Handling Time
- Average Turnout Time
- Average Travel Time
- Average Total Response Time
- Incident Volume by Month
- Cities with Highest Incidents
- Incidents by Category
- Incident Map

This page is designed for quick executive-level review.

---

### 2. Station and Response Performance

This page focuses on station-level and city-level response performance.

It includes:

- Units Available by Station
- Average Response Time by Station
- Response Time by City

This view helps identify stations or cities with higher response times and supports operational resource planning.

---

### 3. Incident Volume Trends

This page analyzes incident patterns by time.

It includes:

- Incident Volume by Hour
- Incident Volume by Day of Week

This view helps identify peak incident hours and high-volume weekdays.

---

### 4. Details Table

The Details Table provides a detailed breakdown by incident category and incident type.

It includes:

- Incident Type Category
- Incident Type
- Total Units
- Total Incidents
- Average Total Response Time
- Average Alarm Time
- Average Travel Time
- Average Turnout Time
- Cold Call %

This page gives users a more detailed tabular view of incident performance metrics.

---

## Key Metrics and Calculations

| Metric | Description | Calculation Logic |
|---|---|---|
| Total Incidents | Count of unique incidents | `COUNTD([Incident No Actual])` |
| Average Alarm Handling Time | Average time from call received to dispatch/alarm | Created in Python fact table, then averaged in Tableau |
| Average Turnout Time | Average time from dispatch/alarm to enroute | Created in Python fact table, then averaged in Tableau |
| Average Travel Time | Average time from enroute to arrival | Created in Python fact table, then averaged in Tableau |
| Average Total Response Time | Average time from call received to arrival | Created in Python fact table, then averaged in Tableau |
| Cold Call % | Percentage of incidents marked as cold response | `COUNTD(IF [Cold Response] = "Yes" THEN [Incident No Actual] END) / COUNTD([Incident No Actual])` |

---

## Response Time Definitions

| Response Time Field | Definition |
|---|---|
| Alarm Handling Time | Time between `PSAP DateTime` and `Alarm DateTime` |
| Turnout Time | Time between `Alarm DateTime` and `Enroute DateTime` |
| Travel Time | Time between `Enroute DateTime` and `Arrival DateTime` |
| Total Response Time | Time between `PSAP DateTime` and `Arrival DateTime` |

All response time values are calculated in minutes.

---

## Data Preparation Process

The raw fire department data was cleaned and transformed using Python before being loaded into Tableau.

Main preparation steps included:

1. Loaded the source Excel file into Python.
2. Standardized column names by removing extra spaces.
3. Converted date/time fields into proper datetime format.
4. Extracted zip code information from incident address.
5. Created city, state, and location-related fields.
6. Removed duplicate records.
7. Created response time fields in minutes.
8. Created a fact table for incident-level analysis.
9. Created supporting dimension tables.
10. Exported cleaned files for Tableau reporting.

---

## Data Model

The dashboard follows a fact and dimension table structure.

### Fact Table

The fact table contains incident-level records and measures such as incident count, station, unit, response times, date/time fields, and location identifiers.

### Dimension Tables

| Dimension Table | Purpose |
|---|---|
| Category Dimension | Stores incident category and incident type details |
| City Dimension | Stores zip code, city, state, and location details |
| Date Dimension | Supports year, month, weekday, and time-based analysis |

---

## Filters Used

The dashboard includes common filters across multiple pages:

| Filter | Description |
|---|---|
| Select Year | Filters the dashboard by year |
| Select Month | Filters the dashboard by month |

The filters allow users to focus on a specific year, month, or all available months.

---

## Data Quality Notes

Some data quality issues were reviewed during the project:

- Some records may have missing station values.
- Some records may have missing date/time values.
- Some response time values may be unusually high.
- Negative response times may indicate incorrect timestamp order in the source data.
- Null month values can appear if date fields are missing.
- City values are based on zip code mapping and should be validated if zip code data is incomplete.

---

## Validation Checklist

Before publishing or sharing the dashboard, the following checks should be completed:

- Confirm total incidents match the cleaned fact table.
- Confirm year and month filters work correctly.
- Confirm KPI values update after filter selection.
- Confirm response time calculations are shown in minutes.
- Confirm the map displays valid locations.
- Confirm the Details Table displays correct incident category and type values.
- Confirm Cold Call % is calculated correctly.
- Confirm navigation buttons work across dashboard pages.
- Confirm the published Tableau dashboard matches the workbook view.

---

## Project Files

Recommended repository structure:

```text
FireDeptAnalysis/
│
├── README.md
├── documentation/
│   └── Fire_Department_Dashboard_Documentation.docx
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── scripts/
│   ├── clean_firedept_data.py
│   ├── create_fact_table.py
│   ├── create_category_dimension.py
│   ├── create_city_dimension.py
│   └── create_date_dimension.py
│
└── tableau/
    └── Fire_Department_Dashboard.twbx
```

---

## How to Use the Dashboard

1. Open the Tableau dashboard.
2. Start with the Summary page.
3. Select the year using the Select Year filter.
4. Select the month using the Select Month filter.
5. Review the KPI cards for high-level performance.
6. Use the Summary page to understand overall incidents, categories, and locations.
7. Use the Station and Response Performance page to review station-level performance.
8. Use the Incident Volume Trends page to analyze incident patterns by hour and weekday.
9. Use the Details Table to review category and incident type-level metrics.

---

## How to Update the Dashboard

1. Add the latest raw data file to the project folder.
2. Run the Python cleaning and transformation scripts.
3. Confirm the cleaned fact and dimension tables are created.
4. Open the Tableau workbook.
5. Refresh the data source.
6. Validate KPI values against the cleaned data.
7. Review filters, charts, and calculated fields.
8. Publish the updated workbook to Tableau Public or Tableau Server.

---

## Dashboard Owner

**Owner:** Anurag Gaonkar  
**Tool:** Tableau  
**Data Preparation:** Python  
**Repository:** FireDeptAnalysis  

---

## Project Status

Initial dashboard development is complete. Future improvements may include adding more data validation checks, improving outlier handling, and adding additional station-level or unit-level drill-down analysis.
