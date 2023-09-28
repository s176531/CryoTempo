import xarray as xr
import numpy as np
from pathlib import Path

our_data = np.load(Path("data/monthly_data/monthly_mean_antarctic.npy"))
phase22_data = xr.open_dataset("data/data_brock_south_hemi/combined_brock_south_hemi/combined_2019_08.nc")

our_mean = np.nanmean(our_data)
phase22_sla_mean = phase22_data.sea_level_anomaly.mean()
phase22_slaf_mean = phase22_data.sea_level_anomaly_filtered.mean()
print(f"Our product: {our_mean*100} cm")
print(f"Phase 2.2 SLA: {phase22_sla_mean.values.item()*100} cm")
print(f"Phase 2.2 SLA filtered: {phase22_slaf_mean.values.item()*100} cm")
