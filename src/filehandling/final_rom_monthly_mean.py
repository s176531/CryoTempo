import numpy as np
import xarray as xr
from pathlib import Path
from tqdm import tqdm

VARIABLES = [
    'sea_level_anomaly',
    'sea_level_anomaly_raw',
    'sea_level_anomaly_filtered',
    'sea_level_anomaly_uncertainty',
    'dynamic_ocean_topography',
    'dynamic_ocean_topography_filtered',
    'dynamic_ocean_topography_uncertainty'
]

def load(folder: Path, file: Path):
    """
    Load arctic and antarctic data from combined nc files.
    Use only the parameters stated in VARIABLES
    """
    data = xr.open_dataset(Path(folder, file))
    return data[VARIABLES]

def get_month(data: xr.DataArray, month: int):
    """Return data for chosen month"""
    if (month < 1) | (month > 12):
        raise ValueError("month should be in the interval [1, 12]")
    months = data.time.values.astype('datetime64[M]').astype(int) % 12 + 1
    return data.isel(time=months==month)

def main():
    """Compute the monthly average of CryoTEMPO phase 2.2 data"""
    data = load(Path("data", "po_tds_c_final"), Path("south_combined.nc"))

    deg_size = .5
    # lat, lon = -62.483333, -59.633333
    lat, lon = -69.0125+deg_size, 39.59
    
    data_area = data.isel(time = (data.latitude < lat+deg_size) & (data.latitude > lat-deg_size) & (data.longitude < lon+deg_size) & (data.longitude > lon-deg_size))

    averages = []
    for month in tqdm(np.arange(1,13)):
        monthly_data = get_month(data_area, month)
        monthly_average = monthly_data.mean(dim="time")
        averages.append(monthly_average)
    all_averages = xr.concat(averages, dim="time")
    all_averages.to_netcdf(Path("data/po_tds_c_final/monthly_averages_syowa.nc"))

if __name__ == "__main__":
    main()