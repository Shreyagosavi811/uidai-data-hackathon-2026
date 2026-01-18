import pandas as pd
import numpy as np


AGE_COLS = ['age_0_5', 'age_5_17', 'age_18_greater']


def normalize_text(df):
    """
    Safe text normalization (won't crash if column missing)
    """
    for col in ['state', 'district']:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )
    return df


def clean_dates(df):
    """
    Standardize date → month_year + year
    """
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df['month_year'] = df['date'].dt.strftime('%m/%Y')
    df['year'] = df['date'].dt.year.astype('Int64')

    df.drop(columns=['date'], inplace=True)
    return df


def clean_age_columns(df):
    """
    Convert age columns and compute total enrolments
    """
    df[AGE_COLS] = df[AGE_COLS].apply(pd.to_numeric, errors='coerce')
    df['number_of_enrolments'] = df[AGE_COLS].sum(axis=1)
    return df


def geo_validate_fast(df, ref):
    """
    Optimized geo validation using dict lookup (BIG DATA SAFE)
    """

    geo_map = {}
    for s, g in ref.groupby('state'):
        geo_map[s] = {}
        for d, sub in g.groupby('district'):
            geo_map[s][d] = set(sub['pincode'])

    def validate(row):
        s, d, p = row['state'], row['district'], str(row['pincode'])
        if s not in geo_map:
            return 'INVALID_STATE'
        if d not in geo_map[s]:
            return 'DISTRICT_STATE_MISMATCH'
        if p not in geo_map[s][d]:
            return 'PINCODE_MISMATCH'
        return 'VALID'

    df['geo_status'] = df.apply(validate, axis=1)
    return df
