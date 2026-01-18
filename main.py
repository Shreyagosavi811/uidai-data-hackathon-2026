import os
from data_loading import load_aadhaar_data, load_reference_data
from cleaning import (
    normalize_text,
    clean_dates,
    clean_age_columns,
    geo_validate_fast,
    AGE_COLS
)

# ---------------- PATHS ---------------- #

BASE_DIR = os.getcwd()

AADHAAR_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
REFERENCE_PATH = os.path.join(BASE_DIR, "data", "reference", "States_UTs.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "output")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ---------------- PIPELINE ---------------- #

print("\n🚀 Starting Aadhaar Data Pipeline\n")

# Load data
df = load_aadhaar_data(AADHAAR_DATA_PATH)
ref = load_reference_data(REFERENCE_PATH)

# Cleaning
df.columns = df.columns.str.lower().str.strip()
df = normalize_text(df)
ref = normalize_text(ref)

df = clean_dates(df)
df = clean_age_columns(df)

# Basic validity filter
df = df[
    (df['state'].notna()) &
    (df['district'].notna()) &
    (df['number_of_enrolments'] > 0)
].copy()

# Geo validation
df = geo_validate_fast(df, ref)

df_valid = df[df['geo_status'] == 'VALID']
df_invalid = df[df['geo_status'] != 'VALID']

# Save intermediate outputs
df_valid.to_csv(os.path.join(OUTPUT_PATH, "validated_records.csv"), index=False)
df_invalid.to_csv(os.path.join(OUTPUT_PATH, "invalid_records.csv"), index=False)

# ---------------- FINAL AGGREGATION ---------------- #

final_df = (
    df_valid
    .groupby(['state', 'district', 'pincode', 'month_year'], as_index=False)[AGE_COLS]
    .sum()
)

final_df.to_csv(
    os.path.join(OUTPUT_PATH, "final_validated_aadhaar_enrolment_dataset.csv"),
    index=False
)

from visualization import run_visualizations
if __name__ == "__main__":
    df_clean = final_df

    # 🔥 THIS LINE IS CRITICAL
    run_visualizations(df_clean, df_invalid)

    print("✅ Pipeline completed successfully")


print("📁 Output folder:", OUTPUT_PATH)
