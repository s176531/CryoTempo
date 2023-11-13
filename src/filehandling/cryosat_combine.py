import xarray as xr
from pathlib import Path
from tqdm import tqdm

# "fix" or "fix_ssb"
prefix = "rads_north_cryotempo" 

# Path to data folder and files
data_folder = Path(f"data/data_{prefix}")
files = list(data_folder.glob("*.nc"))

# Select variables of interest
variables = [
    'sea_level_anomaly',
    'sea_level_anomaly_filtered',
    'sea_level_anomaly_uncertainty'
]

# Subset variables of interest for first day
initial_data = xr.open_dataset(files[0], engine="netcdf4")
combined_data = initial_data[variables]

# Consequtively subset each remaining day and add to data set
for file in tqdm(files[1:]):
    temporary_data = xr.open_dataset(file)
    combined_data = xr.concat((combined_data, temporary_data[variables]), dim="time")

# Sort by time
combined_data = combined_data.sortby("time")

Path(data_folder, f"combined_{prefix}").mkdir(parents=True, exist_ok=True)

# Save to file
combined_data.to_netcdf(Path(data_folder, f"combined_{prefix}", "combined_2019_08.nc"))
