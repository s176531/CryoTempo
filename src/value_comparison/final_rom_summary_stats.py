import numpy as np
import xarray as xr
from pathlib import Path
from tqdm import tqdm

VARIABLES = [
    'sea_level_anomaly',
    'sea_level_anomaly_filtered',
    'sea_level_anomaly_raw',
    'sea_level_anomaly_uncertainty',
    'dynamic_ocean_topography',
    'dynamic_ocean_topography_filtered',
    'dynamic_ocean_topography_uncertainty'
]

def load(folder: Path):
    """
    Load arctic and antarctic data from combined nc files.
    Use only the parameters stated in VARIABLES
    """
    north_data = xr.open_dataset(Path(folder, "north_combined.nc"))
    south_data = xr.open_dataset(Path(folder, "south_combined.nc"))
    
    return north_data[VARIABLES], south_data[VARIABLES]

def summary(data: xr.DataArray):

    mean_all = data.mean()


def get_month(data: xr.DataArray, month: int):
    """Return data for chosen month"""
    if (month < 1) | (month > 12):
        raise ValueError("month should be in the interval [1, 12]")
    months = data.time.values.astype('datetime64[M]').astype(int) % 12 + 1
    return data.isel(time=months==month)


if __name__ == "__main__":
    north_data, south_data = load(Path("data", "po_tds_c_final"))
    south_data_2 = get_month(south_data, 2)
    summary(south_data_2)
    
