import os
import pandas as pd


def load_aadhaar_data(base_path, chunksize=200_000):
    """
    Loads Aadhaar CSV data.
    Supports:
    - Single folder with CSVs
    - Multiple subfolders containing CSVs
    """

    csv_paths = []

    # Walk through base directory
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_paths.append(os.path.join(root, file))

    if not csv_paths:
        raise FileNotFoundError("❌ No CSV files found in Aadhaar data path")

    print(f"📂 Found {len(csv_paths)} CSV files")

    chunks = []
    for path in csv_paths:
        print(f"➡ Loading: {os.path.basename(path)}")
        for chunk in pd.read_csv(path, chunksize=chunksize):
            chunks.append(chunk)

    df = pd.concat(chunks, ignore_index=True)
    print("✅ Aadhaar data loaded:", df.shape)

    return df


def load_reference_data(ref_path):
    """
    Loads UIDAI official State–District–Pincode reference
    """

    if not os.path.exists(ref_path):
        raise FileNotFoundError("❌ Reference file not found")

    ref = pd.read_csv(ref_path)
    ref.columns = ref.columns.str.strip()

    # UIDAI schema → normalized schema
    ref = ref[['stateNameEnglish', 'localBodyNameEnglish', 'pincode']]
    ref.columns = ['state', 'district', 'pincode']

    ref['pincode'] = ref['pincode'].astype(str)
    ref.drop_duplicates(inplace=True)

    print("✅ Reference data loaded:", ref.shape)

    return ref
