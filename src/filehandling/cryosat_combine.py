import xarray as xr
from pathlib import Path
from tqdm import tqdm

PHASE = 1
lat_min, lat_max, lon_min, lon_max = [70, 85, -180, -120]

# Select variables of interest
variables = [
    'sea_level_anomaly',
    'sea_level_anomaly_filtered',
    'sea_level_anomaly_raw'
]

# folder name
folder = f"phase{PHASE}_arctic_all_years" 
# Path to data folder and files
data_folder = Path(f"D:/CryoTempo files/{folder}")
# Make save folder
save_folder_years = Path("data", f"save_folder_Beaufort_phase{PHASE}")
save_folder_years.mkdir(parents=True, exist_ok=True)


for folder in data_folder.glob(f"20[1-2][0-9]"):
    if Path(save_folder_years, f"combined_{folder.stem}.nc").exists():
        continue
    combined_data = []
    for file in tqdm(list(folder.rglob("*.nc"))):
        tmp_data = xr.open_dataset(file)
        beaufort_tmp_data = tmp_data.isel(
            time=(
                    tmp_data.latitude > lat_min
                ) & (
                    tmp_data.latitude < lat_max
                ) & (
                    tmp_data.longitude > lon_min
                ) & (
                    tmp_data.longitude < lon_max
                )
            )

        if len(beaufort_tmp_data.time) > 0:
            combined_data.append(beaufort_tmp_data[variables])

    combined_data = xr.concat(combined_data, dim="time")

    # Sort by time
    combined_data = combined_data.sortby("time")

    # Save to file
    combined_data.to_netcdf(Path(save_folder_years, f"combined_{folder.stem}.nc"))
# for year in tqdm(years, position=0):
#     if Path(save_folder_years, f"combined_{folder}_20{year}.nc").exists():
#         continue
#     files = list(data_folder.glob(f"combined_{folder}_20{year}*.nc"))
#     initial_data = xr.open_dataset(files[0])
#     combined_data = [initial_data[variables]]
    
#     for file in files[1:]:
#         # Consequtively subset each remaining day and add to data set
#         temporary_data = xr.open_dataset(file)
#         combined_data.append(temporary_data[variables])

#     combined_data = xr.concat(combined_data, dim="time")

#         # Sort by time
#     combined_data = combined_data.sortby("time")

#         # Save to file
#     combined_data.to_netcdf(Path(save_folder_years, f"combined_{folder}_20{year}.nc"))

