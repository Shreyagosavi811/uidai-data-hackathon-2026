import os
import matplotlib.pyplot as plt

PLOT_DIR = "output/plots"
os.makedirs(PLOT_DIR, exist_ok=True)


def plot_state_wise_enrollment(df, ref):
    """
    State-wise total Aadhaar enrollments
    (ONLY official states from government reference)
    """

    # Extract official states from gov reference
    official_states = (
        ref["state"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.title()
        .unique()
        .tolist()
    )

    # Filter Aadhaar data to valid states only
    valid_df = df[df["state"].isin(official_states)]

    if valid_df.empty:
        print("⚠ No valid state data found for visualization")
        return

    state_data = (
        valid_df
        .groupby("state")["number_of_enrolments"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(14, 6))
    state_data.plot(kind="bar")

    plt.title("State-wise Aadhaar Enrollments (Official States Only)")
    plt.xlabel("State")
    plt.ylabel("Total Enrollments")
    plt.xticks(rotation=90)
    plt.tight_layout()

    path = os.path.join(PLOT_DIR, "state_wise_enrollment.png")
    plt.savefig(path)
    plt.close()

    print(f"📊 Saved: {path}")


def plot_yearly_enrollment(yearly_df):
    """
    Year-wise total Aadhaar enrollments
    """

    plt.figure(figsize=(10, 5))
    plt.plot(
        yearly_df["year"],
        yearly_df["number_of_enrolments"],
        marker="o"
    )

    plt.title("Year-wise Aadhaar Enrollments")
    plt.xlabel("Year")
    plt.ylabel("Total Enrollments")
    plt.grid(True)
    plt.tight_layout()

    path = os.path.join(PLOT_DIR, "yearly_enrollment.png")
    plt.savefig(path)
    plt.close()

    print(f"📊 Saved: {path}")
