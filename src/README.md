# ApexPlanet Data Analytics Internship - Task 1

## Project Title

Data Immersion & Wrangling

## Objective

The objective of this project is to perform data familiarization, data quality assessment, cleaning, transformation, and validation on the provided sales dataset.

## Dataset Overview

The dataset contains sales transaction information including:

- Order details
- Customer information
- Customer demographics
- Product information
- Quantity and pricing
- Total sales

### Dataset Size

- Records: 1,000
- Columns: 12

## Data Quality Issues Identified

The following issues were identified during the initial data quality assessment:

- 20 missing values in the Age column
- 13 missing values in the City column
- 0 completely duplicate rows
- 8 duplicate Order_ID occurrences
- Order_Date stored as a text/string field

## Data Cleaning Performed

### Missing Age Values

Missing Age values were filled using the median age.

### Missing City Values

Missing City values were first filled using available information from the same customer. Remaining missing values were replaced with "Unknown".

### Duplicate Order IDs

Duplicate Order IDs were made unique by adding suffixes to repeated IDs while preserving all valid transaction records.

### Date Transformation

Order_Date was converted from string format to datetime format.

### Sales Validation

Total_Sales was validated against:

Quantity × Unit_Price

### Outlier Analysis

Potential outliers were identified using the Interquartile Range (IQR) method. They were retained because high sales values may represent legitimate transactions.

## Tools and Technologies

- Python
- Pandas
- NumPy
- OpenPyXL
- Visual Studio Code
- Git and GitHub

## Project Structure

```text
apexplanet_data_analyst/
│
├── data/
│   ├── raw/
│   │   └── ApexPlanet_DataAnalytics_Dataset (1).xlsx
│   │
│   └── processed/
│       └── cleaned_sales_dataset.csv
│
├── docs/
│   └── data_dictionary.md
│
├── src/
│   └── data_cleaning.py
│
├── requirements.txt
├── README.md
└── .gitignore