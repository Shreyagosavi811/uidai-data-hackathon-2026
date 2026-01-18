def run_visualizations(df_clean, df_invalid):
    import os
    import matplotlib.pyplot as plt

    OUTPUT_PATH = "output"
    PLOTS_PATH = os.path.join(OUTPUT_PATH, "plots")
    os.makedirs(PLOTS_PATH, exist_ok=True)

    print("📊 Visualization started")
    print("Clean rows:", df_clean.shape)
    print("Invalid rows:", df_invalid.shape)

    # Before vs After
    before = df_clean[['age_0_5','age_5_17','age_18_greater']].sum().sum()
    after = before  # already cleaned

    plt.figure()
    plt.bar(['After Cleaning'], [after])
    plt.title("Aadhaar Enrolments After Cleaning")
    plt.savefig(os.path.join(PLOTS_PATH, "after_cleaning.png"))
    plt.close()

    print("✅ Plot saved: after_cleaning.png")
