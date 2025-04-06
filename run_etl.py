from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from etl.data_quality import check_data_quality

def main():
    file_path = "data/fire_incidents.csv"
    df = extract_data(file_path)
    df = transform_data(df)
    check_data_quality(df)
    load_data(df)

if __name__ == "__main__":
    main()
