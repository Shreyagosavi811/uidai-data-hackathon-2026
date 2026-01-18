from data_loading import load_raw_data
from cleaning import clean_data
from analysis import analyse_data
from visualization import generate_visuals

def main():
    print("🚀 UIDAI Aadhaar Data Pipeline Started")

    load_raw_data()
    clean_data()
    analyse_data()
    generate_visuals()

    print("🎉 Pipeline completed successfully")

if __name__ == "__main__":
    main()
