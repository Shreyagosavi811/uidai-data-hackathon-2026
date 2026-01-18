# UIDAI Aadhaar Data Analysis – Hackathon 2026

## 📌 Problem Statement
Unlock meaningful societal and administrative insights from Aadhaar enrolment data by identifying trends, anomalies, and quality issues that can support data-driven decision-making and system improvements.

---

## 📊 Dataset Used
- **UIDAI Aadhaar Enrolment Dataset**
- Format: CSV
- Columns used:
  - date
  - state
  - district
  - pincode
  - age_0_5
  - age_5_17
  - age_18_greater

- Reference Dataset:
  - Government State–District–Pincode mapping

---

## 🛠 Project Structure
uidai-data-hackathon-2026/
│
├── data/
│ └── api_data_aadhar_enrollment/
│
├── output/
│ ├── final_validated_aadhaar_enrolment_dataset.csv
│ ├── invalid_records.csv
│ └── plots/
│
├── data_loading.py
├── cleaning.py
├── analysis.py
├── visualization.py
├── main.py
└── README.md

---

## 🔄 Methodology

### 1️⃣ Data Loading
- Memory-efficient chunk loading
- Automatic handling of multiple CSV files and folders

### 2️⃣ Data Cleaning & Validation
- Standardized state and district names
- Removed invalid and duplicate records
- Detected:
  - Invalid states
  - District–state mismatches
  - Pincode mismatches
- Separated valid vs invalid datasets

### 3️⃣ Analysis
- Aggregated enrolments by:
  - State
  - District
  - Pincode
  - Month/Year
- Calculated total enrolments per age group
- Generated year-wise and regional summaries

### 4️⃣ Visualisation
- Before vs after cleaning comparison
- Invalid record distribution
- Year-wise enrolment trend
- Top enrolling states

---

## 📈 Key Insights
- Significant data quality issues exist in raw datasets
- Data cleaning improves analytical reliability
- Aadhaar enrolment shows consistent growth over years
- Certain states dominate enrolment numbers, indicating regional variation

---

## 🎯 Impact & Applicability
- Improves trust in UIDAI analytics
- Helps administrators identify data-entry issues
- Supports policy decisions through clean trends
- Framework can be reused for other government datasets

---

## ▶️ How to Run
```bash
pip install pandas matplotlib numpy
python main.py
Visualisations will be saved in:
output/plots/
