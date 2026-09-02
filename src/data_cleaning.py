import pandas as pd
import numpy as np
import os

# ============================================================
# APEXPLANET DATA ANALYTICS INTERNSHIP
# TASK 1: DATA IMMERSION & WRANGLING
# ============================================================


# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

file_path = "data/raw/ApexPlanet_DataAnalytics_Dataset (1).xlsx"

print("\n" + "=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_excel(file_path)

print("\nDataset loaded successfully!")
print("Dataset shape:", df.shape)


# ------------------------------------------------------------
# 2. DATA FAMILIARIZATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head())

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA TYPES BEFORE CLEANING ---")
print(df.dtypes)

print("\n--- SUMMARY STATISTICS ---")
print(df.describe(include="all"))


# ------------------------------------------------------------
# 3. DATA QUALITY ASSESSMENT
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA QUALITY ASSESSMENT")
print("=" * 60)

print("\n--- MISSING VALUES BEFORE CLEANING ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print("Number of duplicate rows:", df.duplicated().sum())

print("\n--- DUPLICATE ORDER IDs ---")
print("Number of duplicate Order IDs:",
      df["Order_ID"].duplicated().sum())


# ------------------------------------------------------------
# 4. CLEAN MISSING AGE VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING AGE")
print("=" * 60)

median_age = df["Age"].median()

df["Age"] = df["Age"].fillna(median_age)

print("Median age used:", median_age)
print("Remaining missing Age values:",
      df["Age"].isnull().sum())


# ------------------------------------------------------------
# 5. CLEAN MISSING CITY VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING CITY")
print("=" * 60)

# Try to fill missing City using the same customer's known city
df["City"] = df.groupby("Customer_ID")["City"].transform(
    lambda x: x.fillna(x.mode().iloc[0])
    if not x.mode().empty else x
)

# Remaining missing values become Unknown
df["City"] = df["City"].fillna("Unknown")

print("Remaining missing City values:",
      df["City"].isnull().sum())


# ------------------------------------------------------------
# 6. FIX DUPLICATE ORDER IDs
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FIXING DUPLICATE ORDER IDs")
print("=" * 60)

print("Duplicate Order IDs before:",
      df["Order_ID"].duplicated().sum())

# Add suffix to repeated Order IDs
df["Order_ID"] = [
    order_id if count == 0 else f"{order_id}_{count}"
    for order_id, count in zip(
        df["Order_ID"],
        df.groupby("Order_ID").cumcount()
    )
]

print("Duplicate Order IDs after:",
      df["Order_ID"].duplicated().sum())


# ------------------------------------------------------------
# 7. CLEAN ORDER DATE
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING ORDER DATE")
print("=" * 60)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

print("Missing/Invalid Order Dates:",
      df["Order_Date"].isnull().sum())

print("Order_Date datatype:",
      df["Order_Date"].dtype)

print("Earliest date:", df["Order_Date"].min())
print("Latest date:", df["Order_Date"].max())


# ------------------------------------------------------------
# 8. VALIDATE TOTAL SALES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("VALIDATING TOTAL SALES")
print("=" * 60)

# Calculate expected sales
df["Calculated_Sales"] = (
    df["Quantity"] * df["Unit_Price"]
)

# Find mismatches
sales_mismatch = df[
    ~np.isclose(
        df["Total_Sales"],
        df["Calculated_Sales"],
        rtol=0.01
    )
]

print("Total sales calculation mismatches:",
      len(sales_mismatch))

# Remove temporary column
df.drop(columns=["Calculated_Sales"], inplace=True)


# ------------------------------------------------------------
# 9. CHECK OUTLIERS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("OUTLIER ANALYSIS")
print("=" * 60)

Q1 = df["Total_Sales"].quantile(0.25)
Q3 = df["Total_Sales"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[
    (df["Total_Sales"] < lower_bound) |
    (df["Total_Sales"] > upper_bound)
]

print("Potential Total_Sales outliers:",
      len(outliers))

print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)

print(
    "\nNote: Outliers were not automatically removed "
    "because high sales values may represent legitimate transactions."
)


# ------------------------------------------------------------
# 10. FINAL DATA VALIDATION
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATA VALIDATION")
print("=" * 60)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nDuplicate rows after cleaning:",
      df.duplicated().sum())

print("Duplicate Order IDs after cleaning:",
      df["Order_ID"].duplicated().sum())

print("\nFinal dataset shape:", df.shape)


# ------------------------------------------------------------
# 11. SAVE CLEANED DATASET
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("SAVING CLEANED DATASET")
print("=" * 60)

# Create processed folder if it does not exist
os.makedirs("data/processed", exist_ok=True)

output_file = "data/processed/cleaned_sales_dataset.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nCleaned dataset saved successfully!")
print("File location:", output_file)

print("\n" + "=" * 60)
print("TASK 1 COMPLETED SUCCESSFULLY")
print("=" * 60)

