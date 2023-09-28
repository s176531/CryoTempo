import xarray as xr
from pathlib import Path
from tqdm import tqdm
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmcrameri.cm as cmc

# "fix" or "fix_ssb"
prefix = "fix_ssb" 

# Path to data folder and files
file = Path(f"data/data_investigate_offset/combined.nc")
data = xr.open_dataset(file)

data["sea_level_anomaly_plus_dynamic_atmosphere"] = data.sea_level_anomaly + data.dynamic_atmosphere
data["sea_level_anomaly_minus_dynamic_atmosphere"] = data.sea_level_anomaly - data.dynamic_atmosphere
data["sea_level_anomaly_filtered_plus_dynamic_atmosphere"] = data.sea_level_anomaly_filtered + data.dynamic_atmosphere
data["sea_level_anomaly_filtered_minus_dynamic_atmosphere"] = data.sea_level_anomaly_filtered - data.dynamic_atmosphere

vars = [
    "sea_level_anomaly_plus_dynamic_atmosphere",
    "sea_level_anomaly_minus_dynamic_atmosphere",
    "sea_level_anomaly_filtered_plus_dynamic_atmosphere",
    "sea_level_anomaly_filtered_minus_dynamic_atmosphere"
]

for var in tqdm(vars):
    fig = plt.figure(figsize=(13,8), dpi=300)
    ax = fig.add_subplot(1,1,1, projection=ccrs.SouthPolarStereo())
    im = ax.scatter(data.longitude, data.latitude, c=data[var], s=0.005, alpha=0.3, cmap=cmc.vik, transform=ccrs.Geodetic(), vmin=-.5, vmax=.5)
    ax.coastlines()
    cbar = fig.colorbar(im)
    cbar.set_label("SLA [m]", fontsize=14)
    cbar.solids.set(alpha=1)
    title_string = var.replace("_", " ")
    ax.set_title(f"{title_string} August 2019", fontsize=20)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    plt.savefig(Path("figures", f"investigate_offset", f"{var}.png"))
    plt.close()
