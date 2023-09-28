import xarray as xr
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
import cartopy.crs as ccrs
import numpy as np

from pathlib import Path

file = Path("../scratch_copy/data_v6/v6_mss21.nc")
data = xr.open_dataset(file)
data = data.isel(time=(data.time >= np.datetime64("2019-08-01")) & (data.time <= np.datetime64("2019-09-01")))
data = data.isel(lats=data.Latitude[:,0] <= -45)
mean_data = np.nanmean(data.sla21, axis=0)

fig = plt.figure(figsize=(13,8), dpi=300)
ax = fig.add_subplot(1,1,1, projection=ccrs.SouthPolarStereo())
im = ax.scatter(data.Longitude, data.Latitude, c=mean_data, s=8, cmap=cmc.vik, transform=ccrs.Geodetic(), vmin=-0.5, vmax=0.5)
ax.coastlines()
cbar = fig.colorbar(im)
cbar.set_label("SLA [m]", fontsize=14)
cbar.solids.set(alpha=1)
ax.set_title(f"Data product sea level anomaly August 2019", fontsize=20)
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.savefig(Path("figures", "our_data_2019_08", f"sea_level_anomaly.png"))
plt.close()

