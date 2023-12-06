import numpy as np
import xarray as xr
from pathlib import Path
from tqdm import tqdm

MAIN_FOLDER = Path("data/po_tds_c_final")

VERSION = "l2-test"
MONTHS = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

def main():
    for MONTH in MONTHS:
        # north_folder = Path(MAIN_FOLDER, "nh", VERSION)
        south_folder = Path(MAIN_FOLDER, "sh", VERSION, "2019", MONTH)

        # north_data = []
        # for file in tqdm(list(north_folder.rglob("*nc"))):
        #     north_data.append(xr.open_dataset(file))
        # north_data_concat = xr.concat(north_data, dim="time")
        # north_data_concat.sortby("time")
        # north_data_concat.to_netcdf(MAIN_FOLDER, f"{VERSION}_north_combined.nc")
        # del north_data_concat, north_data
    
        south_data = []
        for file in tqdm(list(south_folder.rglob("*nc"))):
            south_data.append(xr.open_dataset(file))
        print("Concatenating")
        south_data_concat = xr.concat(south_data, dim="time")
        print("Sorting by time")
        south_data_concat.sortby("time")
        print("Saving compiled file")
        south_data_concat.to_netcdf(Path(MAIN_FOLDER, f"{VERSION}_south_combined_{MONTH}.nc"))

def combine_year(pole: str = "south"):
    """Combine monthly .nc files for either north or south pole"""
    folder = Path(MAIN_FOLDER, pole)

    glob = list(folder.glob("*.nc"))
    combined_data = xr.open_dataset(glob[0])
    for file in tqdm(glob[1:]):
        temp_data = xr.open_dataset(file)
        combined_data = xr.concat([combined_data, temp_data], dim="time")
    data_sorted = combined_data.sortby("time")
    data_sorted.to_netcdf(Path(MAIN_FOLDER, f"{pole}_combined.nc"))

if __name__ == "__main__":
    combine_year("north")