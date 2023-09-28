import xarray as xr
from pathlib import Path
import numpy as np

save_path = Path("data/monthly_data")
save_path.mkdir(parents=True, exist_ok=True)
file = Path(r"C:\Users\mathi\OneDrive\Dokumenter\DTU\Research Assistant\scratch_copy\data_v6", "v6_mss21.nc")
data = xr.open_dataset(file)

# filter time
year_idx = data.time.values.astype("datetime64[Y]").astype(int) + 1970 == 2019
data_year = data.isel(time = year_idx)

# filter latitude
lat_idx = data.Latitude[:,0] <= -60
data_filtered = data_year.isel(lats = lat_idx)

# average of each month may -> october
# monthly_mean = np.full((6, data_filtered.sla21.shape[1], data_filtered.sla21.shape[2]), np.nan)
monthly_mean = np.full((data_filtered.sla21.shape[1], data_filtered.sla21.shape[2]), np.nan)
# for i in range(1):
t_idx = data_filtered.time.values.astype("datetime64[M]").astype(int) % 12 == 8
monthly_mean = np.nanmean(data_filtered.sla21.values[t_idx], axis=0)

np.save(Path(save_path, "monthly_mean_antarctic.npy"), monthly_mean)
