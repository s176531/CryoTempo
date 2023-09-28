import xarray as xr
from pathlib import Path
import pandas as pd

lims_north = [55, 75]
lims_south = [-55, -75]

north_file = Path("data/data_brock_north_hemi/combined_brock_north_hemi/combined_2019_08.nc")
south_file = Path("data/data_brock_south_hemi/combined_brock_south_hemi/combined_2019_08.nc")
rads_file = Path("data/cryo")

north_data = xr.open_dataset(north_file)
south_data = xr.open_dataset(south_file)
rads_data = pd.read_csv(rads_file, sep=" ", skipinitialspace=True, names=["ID", "latitude", "longitude", "dec_year", "sea_level_anomaly"], usecols=[0,1,2,3,4])
rads_data.longitude[rads_data["longitude"]>180] -= 360

rads_band_north = rads_data.sea_level_anomaly[(rads_data.latitude > lims_north[0]) & (rads_data.latitude < lims_north[1])]
rads_band_south = rads_data.sea_level_anomaly[(rads_data.latitude < lims_south[0]) & (rads_data.latitude > lims_south[1])]
phase22_band_north = north_data.sea_level_anomaly.isel(time = (north_data.latitude > lims_north[0]) & (north_data.latitude < lims_north[1]))
phase22_band_south = south_data.sea_level_anomaly.isel(time = (south_data.latitude < lims_south[0]) & (south_data.latitude > lims_south[1]))

rads_mean_north = rads_band_north.mean()
rads_mean_south = rads_band_south.mean()
phase22_mean_north = phase22_band_north.mean()
phase22_mean_south = phase22_band_south.mean()

print("\n")
print(f"Offset Arctic data for latitudes ({lims_north[0]}, {lims_north[1]}): {(rads_mean_north-phase22_mean_north.item())*100} cm")
print(f"Points in RADS data: {len(rads_band_north)}")
print(f"Points in Phase2.2 data: {len(phase22_band_north)}")
print("\n")
print(f"Offset Antarctic data for latitudes ({lims_south[0]}, {lims_south[1]}): {(rads_mean_south-phase22_mean_south.item())*100} cm")
print(f"Points in RADS data: {len(rads_band_south)}")
print(f"Points in Phase2.2 data: {len(phase22_band_south)}")