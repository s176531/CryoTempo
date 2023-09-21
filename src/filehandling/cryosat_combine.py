import xarray as xr
from pathlib import Path
from tqdm import tqdm

# Path to data folder and files
data_folder = Path("data")
files = list(data_folder.glob("*.nc"))

# Select variables of interest
variables = [
    'sea_level_anomaly',
    'sea_level_anomaly_filtered',
    'sea_level_anomaly_raw',
    'sea_level_anomaly_uncertainty',
    'sea_state_bias',
    'inverse_barometric'
]

# Subset variables of interest for first day
initial_data = xr.open_dataset(files[0])
combined_data = initial_data[variables]

# Consequtively subset each remaining day and add to data set
for file in tqdm(files[1:]):
    temporary_data = xr.open_dataset(file)
    combined_data = xr.concat((combined_data, temporary_data[variables]), dim="time")

# Sort by time
combined_data = combined_data.sortby("time")

Path(data_folder, "combined").mkdir(parents=True, exist_ok=True)

# Save to file
combined_data.to_netcdf(Path(data_folder, "combined", "combined_2019_08.nc"))
