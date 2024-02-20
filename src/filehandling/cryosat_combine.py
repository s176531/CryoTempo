import xarray as xr
from pathlib import Path
from tqdm import tqdm

# Select variables of interest
variables = [
    'sea_level_anomaly',
    'sea_level_anomaly_filtered',
    'sea_level_anomaly_uncertainty',
    'sea_level_anomaly_raw'
]

# folder name
folder = "phase21_arctic_all_years" 
# Path to data folder and files
data_folder = Path(f"data/{folder}")
# Make save folder
save_folder_years = Path(data_folder, "save_folder_years")
save_folder_years.mkdir(parents=True, exist_ok=True)


years = list(range(10,22))

for year in tqdm(years, position=0):
    if Path(save_folder_years, f"combined_{folder}_20{year}.nc").exists():
        continue
    files = list(data_folder.glob(f"combined_{folder}_20{year}*.nc"))
    initial_data = xr.open_dataset(files[0])
    combined_data = [initial_data[variables]]
    
    for file in files[1:]:
        # Consequtively subset each remaining day and add to data set
        temporary_data = xr.open_dataset(file)
        combined_data.append(temporary_data[variables])

    combined_data = xr.concat(combined_data, dim="time")

        # Sort by time
    combined_data = combined_data.sortby("time")

        # Save to file
    combined_data.to_netcdf(Path(save_folder_years, f"combined_{folder}_20{year}.nc"))

