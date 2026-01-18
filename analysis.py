# analysis.py
def validate_geo(df, ref):
    state_district = ref.groupby('state')['district'].apply(set).to_dict()

    def check(row):
        if row['state_corrected'] not in state_district:
            return 'INVALID_STATE'
        if row['district_corrected'] not in state_district[row['state_corrected']]:
            return 'DISTRICT_STATE_MISMATCH'
        return 'VALID'

    df['geo_status'] = df.apply(check, axis=1)
    return df


def merge_age_data(df, age_df):
    return df.merge(
        age_df,
        on=['state', 'district', 'pincode'],
        how='left'
    )
