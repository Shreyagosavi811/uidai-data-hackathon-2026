import os
import pandas as pd

# ==================================================
# OFFICIAL STATE / UT RENAMING MAP (Govt of India)
# ==================================================
STATE_RENAME_MAP = {
    "orissa": "odisha",
    "pondicherry": "puducherry",
    "uttaranchal": "uttarakhand",
    "andaman & nicobar": "andaman and nicobar islands",
    "andaman and nicobar": "andaman and nicobar islands",
    "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
    "daman & diu": "dadra and nagar haveli and daman and diu",
    "jammu & kashmir": "jammu and kashmir",
    "nct of delhi": "delhi"
}


# ==================================================
# LOAD AADHAAR DATA
# ==================================================
def load_aadhaar_data(base_path, chunksize=200_000):
    """
    Loads Aadhaar CSV data from folders/subfolders
    """

    csv_paths = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_paths.append(os.path.join(root, file))

    if not csv_paths:
        raise FileNotFoundError("❌ No CSV files found in Aadhaar data path")

    print(f"📂 Found {len(csv_paths)} Aadhaar CSV files")

    chunks = []
    for path in csv_paths:
        print(f"➡ Loading: {os.path.basename(path)}")
        for chunk in pd.read_csv(path, chunksize=chunksize):
            chunks.append(chunk)

    df = pd.concat(chunks, ignore_index=True)
    print("✅ Aadhaar data loaded:", df.shape)

    return df


# ==================================================
# LOAD GOVERNMENT REFERENCE DATA
# ==================================================
def load_reference_data(ref_path):
    """
    Loads UIDAI official State–District–Pincode reference
    """

    if os.path.isdir(ref_path):
        csv_files = [f for f in os.listdir(ref_path) if f.endswith(".csv")]
        if not csv_files:
            raise FileNotFoundError("❌ No CSV found in reference directory")
        ref_path = os.path.join(ref_path, csv_files[0])

    ref = pd.read_csv(ref_path)
    ref.columns = ref.columns.str.strip()

    ref = ref[['stateNameEnglish', 'localBodyNameEnglish', 'pincode']]
    ref.columns = ['state', 'district', 'pincode']

    ref['state'] = ref['state'].str.lower().str.strip()
    ref['pincode'] = ref['pincode'].astype(str)

    ref.drop_duplicates(inplace=True)

    print("✅ Reference data loaded:", ref.shape)

    return ref


# ==================================================
# STATE VALIDATION + UT RENAMING + AUDIT
# ==================================================
def validate_and_fix_states(df, ref_df, output_dir="output"):
    """
    - Fix state name mismatches (UT renaming)
    - Keep only valid Govt states
    - Generate audit CSVs
    """

    os.makedirs(output_dir, exist_ok=True)

    # normalize Aadhaar state
    df['state_original'] = df['state']
    df['state'] = (
        df['state']
        .str.lower()
        .str.strip()
        .replace(STATE_RENAME_MAP)
    )

    valid_states = set(ref_df['state'].unique())

    # mark validity
    df['state_valid'] = df['state'].isin(valid_states)

    # -------------------------
    # AUDIT FILES
    # -------------------------
    valid_states_df = (
        df[df['state_valid']]
        [['state']]
        .drop_duplicates()
        .sort_values('state')
    )

    invalid_states_df = (
        df[~df['state_valid']]
        [['state_original', 'state']]
        .drop_duplicates()
        .sort_values('state_original')
    )

    valid_states_df.to_csv(
        os.path.join(output_dir, "valid_states.csv"),
        index=False
    )

    invalid_states_df.to_csv(
        os.path.join(output_dir, "invalid_states_audit.csv"),
        index=False
    )

    print(f"✅ Valid states saved: output/valid_states.csv")
    print(f"⚠ Invalid states audit saved: output/invalid_states_audit.csv")

    # return ONLY valid records for analysis & plots
    return df[df['state_valid']].copy()
