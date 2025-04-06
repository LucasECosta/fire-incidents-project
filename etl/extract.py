import pandas as pd
import os

def extract_data(file_path: str) -> pd.DataFrame:
    # If the file does not exist locally, download it from the internet
    if not os.path.exists(file_path):
        print("Downloading the dataset...")
        url = "https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD"
        df = pd.read_csv(url, low_memory=False)
        df.to_csv(file_path, index=False)
    else:
        print("Reading the local dataset...")
        df = pd.read_csv(file_path, low_memory=False)

    return df
