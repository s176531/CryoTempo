import xarray as xr
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
import cartopy.crs as ccrs

from pathlib import Path

# "fix" or "fix_ssb"
prefix = "brock_south_hemi"

file = Path(f"data/data_{prefix}/combined_{prefix}/combined_2019_08.nc")
data = xr.load_dataset(file)
vars = list(data.data_vars)
Path("figures", f"cryosat_2019_08_{prefix}").mkdir(parents=True, exist_ok=True)

# sla, filtered sla, sla uncertainty
cmaps = [cmc.vik, cmc.vik, cmc.lajolla_r]
cbar_labels = ["SLA [m]", "SLA [m]", r"$\Delta$SLA [m]"]

for var, cmap, cbar_label in zip(vars, cmaps, cbar_labels):
    fig = plt.figure(figsize=(13,8), dpi=300)
    ax = fig.add_subplot(1,1,1, projection=ccrs.SouthPolarStereo())
    im = ax.scatter(data.longitude, data.latitude, c=data[var], s=0.005, alpha=0.3, cmap=cmap, transform=ccrs.Geodetic(), vmin=-.5, vmax=.5)
    ax.coastlines()
    cbar = fig.colorbar(im)
    cbar.set_label(cbar_label, fontsize=14)
    cbar.solids.set(alpha=1)
    title_string = var.replace("_", " ")
    ax.set_title(f"{title_string} August 2019 phase 2.2", fontsize=20)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    plt.savefig(Path("figures", f"cryosat_2019_08_{prefix}", f"{var}.png"))
    plt.close()

