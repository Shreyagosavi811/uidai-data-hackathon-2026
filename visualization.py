import os
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_PATH = "output"
FINAL_DATASET = os.path.join(OUTPUT_PATH, "final_validated_aadhaar_enrolment_dataset.csv")
INVALID_DATASET = os.path.join(OUTPUT_PATH, "invalid_records.csv")

os.makedirs(os.path.join(OUTPUT_PATH, "plots"), exist_ok=True)

# -----------------------------
# Load datasets
# -----------------------------
df_final = pd.read_csv(FINAL_DATASET)
df_invalid = pd.read_csv(INVALID_DATASET)

AGE_COLS = ['age_0_5', 'age_5_17', 'age_18_greater']


# -----------------------------
# 1. Before vs After Cleaning
# -----------------------------
before_total = df_final[AGE_COLS].sum().sum() + df_invalid[AGE_COLS].sum().sum()
after_total = df_final[AGE_COLS].sum().sum()

plt.figure()
plt.bar(['Before Cleaning', 'After Cleaning'], [before_total, after_total])
plt.title("Aadhaar Enrolments: Before vs After Cleaning")
plt.ylabel("Total Enrolments")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "plots", "before_after_cleaning.png"))
plt.close()


# -----------------------------
# 2. Invalid Records Breakdown
# -----------------------------
if 'geo_status' in df_invalid.columns:
    invalid_counts = df_invalid['geo_status'].value_counts()

    plt.figure()
    invalid_counts.plot(kind='bar')
    plt.title("Invalid Records by Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, "plots", "invalid_record_types.png"))
    plt.close()


# -----------------------------
# 3. Year-wise Enrolment Trend
# -----------------------------
df_final['year'] = df_final['month_year'].astype(str).str[-4:]

yearly_trend = (
    df_final
    .groupby('year')[AGE_COLS]
    .sum()
    .sum(axis=1)
)

plt.figure()
yearly_trend.plot(marker='o')
plt.title("Year-wise Aadhaar Enrolment Trend")
plt.ylabel("Total Enrolments")
plt.xlabel("Year")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "plots", "yearly_trend.png"))
plt.close()


# -----------------------------
# 4. Top 10 States by Enrolment
# -----------------------------
state_totals = (
    df_final
    .groupby('state')[AGE_COLS]
    .sum()
    .sum(axis=1)
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
state_totals.plot(kind='bar')
plt.title("Top 10 States by Aadhaar Enrolment")
plt.ylabel("Total Enrolments")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "plots", "top_10_states.png"))
plt.close()


print("✅ All visualizations generated in output/plots/")
