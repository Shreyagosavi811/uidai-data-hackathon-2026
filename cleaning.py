import pandas as pd
import numpy as np

AGE_COLS = ['age_0_5', 'age_5_17', 'age_18_greater']


def normalize_text(df):
    """
    Normalize text columns safely
    """
    df = df.copy()

    for col in ['state', 'district']:
        if col in df.columns:
            df.loc[:, col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )
    return df


def clean_dates(df):
    """
    Convert date column → month_year + year
    SAFE for sliced DataFrames
    """
    df = df.copy()

    if 'date' not in df.columns:
        return df

    # Convert date safely
    date_series = pd.to_datetime(df['date'], errors='coerce')

    df.loc[:, 'month_year'] = date_series.dt.to_period('M').astype(str)
    df.loc[:, 'year'] = date_series.dt.year.astype('Int64')

    # Drop raw date (optional but recommended)
    df.drop(columns=['date'], inplace=True)

    return df


def clean_age_columns(df):
    """
    Convert age columns to numeric & compute total enrollments
    NEVER returns None
    """
    df = df.copy()

    # Use only columns that exist
    existing_age_cols = [c for c in AGE_COLS if c in df.columns]

    if not existing_age_cols:
        # If age columns missing, still create total column
        df.loc[:, 'number_of_enrolments'] = 0
        return df

    # Convert to numeric safely
    df.loc[:, existing_age_cols] = (
        df[existing_age_cols]
        .apply(pd.to_numeric, errors='coerce')
        .fillna(0)
    )

    # Compute total
    df.loc[:, 'number_of_enrolments'] = df[existing_age_cols].sum(axis=1)

    return df


def geo_validate_fast(df, ref):
    """
    Optimized geo validation (dict-based lookup)
    Suitable for large datasets
    """
    df = df.copy()

    geo_map = {}
    for s, g in ref.groupby('state'):
        geo_map[s] = {}
        for d, sub in g.groupby('district'):
            geo_map[s][d] = set(sub['pincode'].astype(str))

    def validate(row):
        s = row.get('state')
        d = row.get('district')
        p = str(row.get('pincode'))

        if s not in geo_map:
            return 'INVALID_STATE'
        if d not in geo_map[s]:
            return 'DISTRICT_STATE_MISMATCH'
        if p not in geo_map[s][d]:
            return 'PINCODE_MISMATCH'
        return 'VALID'

    df.loc[:, 'geo_status'] = df.apply(validate, axis=1)
    return df
