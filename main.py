import os
import pandas as pd

from data_loading import (
    load_aadhaar_data,
    load_reference_data,
    validate_and_fix_states
)

from cleaning import (
    normalize_text,
    clean_dates,
    clean_age_columns
)
from visualization import (
    plot_state_wise_enrollment,
    plot_yearly_enrollment
)

# ==========================
# PATH CONFIG
# ==========================
AADHAAR_DATA_PATH = "data/raw"
REFERENCE_DATA_PATH = "data/reference"   # <-- GOV reference folder
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================
# LOAD DATA
# ==========================
print("📥 Loading Aadhaar data...")
df = load_aadhaar_data(AADHAAR_DATA_PATH)

print("📥 Loading Government reference data...")


REFERENCE_DATA_PATH = "data/reference"

ref = load_reference_data(REFERENCE_DATA_PATH)

df = validate_and_fix_states(
    df,
    ref,
    output_dir=OUTPUT_DIR
)


# ==========================
# CLEANING PIPELINE
# ==========================
print("🧹 Normalizing text...")
df = normalize_text(df)
ref = normalize_text(ref)

print("📅 Cleaning dates...")
df = clean_dates(df)

print("👶 Cleaning age columns & computing total enrollments...")
df = clean_age_columns(df)

# ==========================
# SAVE CLEANED DATA
# ==========================
cleaned_path = os.path.join(OUTPUT_DIR, "cleaned_aadhaar.csv")
df.to_csv(cleaned_path, index=False)
print(f"✅ Cleaned data saved: {cleaned_path}")

# ==========================
# YEAR-WISE ENROLLMENT CSV
# ==========================
print("📊 Computing yearly enrollment...")

yearly_df = (
    df.groupby("year", dropna=True)["number_of_enrolments"]
    .sum()
    .reset_index()
)

yearly_csv_path = os.path.join(OUTPUT_DIR, "yearly_enrollment.csv")
yearly_df.to_csv(yearly_csv_path, index=False)

print(f"📊 Year-wise enrollment saved: {yearly_csv_path}")

# ==========================
# VISUALIZATIONS (VALID STATES ONLY)
# ==========================
print("📈 Generating visualizations...")
plot_state_wise_enrollment(df, ref)   # ✅ Option A applied
plot_yearly_enrollment(yearly_df)

print("🎉 Project executed successfully!")
