import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
import cartopy.crs as ccrs
import numpy as np

from pathlib import Path

file = Path("data/monthly_data/monthly_mean.npy")
savepath = Path("figures", "monthly_means")
savepath.mkdir(parents=True, exist_ok=True)
data = np.load(file)
lats = np.linspace(45.5,89.5, data.shape[1])
lons = np.linspace(-179.5,179.5, data.shape[2])
lon, lat = np.meshgrid(lons, lats)

months = {0: "May", 1: "June", 2: "July", 3: "August", 4: "September", 5: "October"}
for i in range(6):
    fig = plt.figure(figsize=(13,8), dpi=300)
    ax = fig.add_subplot(1,1,1, projection=ccrs.NorthPolarStereo())
    im = ax.scatter(lon, lat, c=data[i], s=8, cmap=cmc.vik, transform=ccrs.Geodetic(), vmin=-0.5, vmax=0.5)
    ax.coastlines()
    cbar = fig.colorbar(im)
    cbar.set_label("SLA [m]", fontsize=14)
    cbar.solids.set(alpha=1)
    ax.set_title(f"Data product Artic SLA {months[i]} 2015", fontsize=20)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    plt.savefig(Path(savepath, f"monthly_mean_{months[i]}.png"))
    plt.close()

