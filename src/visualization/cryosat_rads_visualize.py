import pandas as pd
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
import cartopy.crs as ccrs

from pathlib import Path

file = Path("data/cryo")
data = pd.read_csv(file, sep=" ", skipinitialspace=True, names=["ID", "latitude", "longitude", "dec_year", "sea_level_anomaly"], usecols=[0,1,2,3,4])
# data["longitude"] -= 180
data = data[data.latitude <= -45]
# data = xr.load_dataset(file, engine="netcdf4")


fig = plt.figure(figsize=(13,8), dpi=300)
ax = fig.add_subplot(1,1,1, projection=ccrs.SouthPolarStereo())
im = ax.scatter(data.longitude, data.latitude, c=data.sea_level_anomaly, s=0.05, alpha=0.5, cmap=cmc.vik, transform=ccrs.Geodetic(), vmin=-0.5, vmax=0.5)
ax.coastlines()
cbar = fig.colorbar(im)
cbar.set_label("SLA [m]", fontsize=14)
cbar.solids.set(alpha=1)
ax.set_title(f"RADS sea level anomaly August 2019", fontsize=20)
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.savefig(Path("figures", "cryosat_2019_08_rads", f"sea_level_anomaly.png"))
plt.close()

