# download assets using S3

import requests
import os
from dep_tools.grids import get_tiles

# https://data.digitalearthpacific.org/

regions = "FJI"

product = "dep_s2_mangroves"
version = "0-2-0"
years = range(2017, 2025)
bands = ["mangroves"]

# product = "dep_s2_geomad"
# version = "0-4-0"
# years = [2024]
# bands = ["blue", 'red', 'green', 'nir', 'nir08', 'nir09', 'swir16', 'swir22', 'rededge1', 'rededge2', 'rededge3']

s3_url = "https://s3.us-west-2.amazonaws.com/dep-public-data"


def download_if_not_exists(url, filepath):
    if not os.path.exists(filepath):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filepath, mode="wb") as file:
                for chunk in response.iter_content(chunk_size=10 * 1024):
                    file.write(chunk)
            print(f"Data downloaded and saved to: {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        pass


# main
country_codes = None if regions.upper() == "ALL" else regions.split(",")

tiles = get_tiles(country_codes=country_codes)
tiles = list(tiles)

print(f"Tiles : {len(tiles)}")

for year in years:
    # print(year)
    for t in tiles:
        for band in bands:
            url = f"{s3_url}/{product}/{version}/{t[0][0]:03d}/{t[0][1]:03d}/{year}/{product}_{t[0][0]:03d}_{t[0][1]:03d}_{year}_{band}.tif"
            file_name = f"{product}_{t[0][0]:03d}_{t[0][1]:03d}_{year}_{band}.tif"
            folder = f"data/{product}/{regions}/{year}"
            if not os.path.exists(folder):
                os.makedirs(folder)
            # print(file_name)
            download_if_not_exists(url, f"{folder}/{file_name}")
