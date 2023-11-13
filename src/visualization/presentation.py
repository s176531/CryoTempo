import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path
import cmcrameri.cm as cmc

base_path = Path(r"C:\Users\mathi\Danmarks Tekniske Universitet\Casper Tygesen Bang-Hansen - ProcessedGrids")

measures = xr.open_dataset(Path(base_path, "MEaSUREs", "ssh_grids_v2205_2019050212.nc"))
sla = measures.SLA.values[0]
measures_sla = np.hstack([sla[:,sla.shape[1]//2:], sla[:,:sla.shape[1]//2]])

cmems = xr.open_dataset(Path(base_path, "CMEMS", "dt_global_twosat_phy_l4_20190502_vDT2021.nc"))
cmems = cmems.isel(latitude = abs(cmems.latitude) < 80)

# our = xr.open_dataset(Path(base_path, "Processed_v6_v01", "2019_5_2.nc"))
our = xr.open_dataset(Path(base_path, "v6_mss21.nc"))
our = our.isel(time = our.time == np.datetime64("2019-05-02T12:00:00.000000000"))
our = our.isel(lats = abs(our.Latitude[:,0] < 80))


labelsize = 14
titlesize = 20

plt.figure(figsize=(12,5), dpi=500)
plt.imshow(cmems.sla[0]*100, origin="lower", extent=[-180,180,-80,80], cmap=cmc.vik, vmin=-50, vmax=50)
cbar=plt.colorbar()
cbar.set_label("SLA [m]", fontsize=labelsize)
plt.title("CMEMS sea level anomaly 2019-05-02", fontsize=titlesize)
plt.xlabel(f"Longitude [\N{DEGREE SIGN}]", fontsize=labelsize)
plt.ylabel(f"Latitude [\N{DEGREE SIGN}]", fontsize=labelsize)
plt.savefig(Path("figures", "presentation", "cmems.png"))
plt.close()

plt.figure(figsize=(12,5), dpi=500)
plt.imshow(measures_sla*100, origin="lower", extent=[-180,180,-80,80], cmap=cmc.vik, vmin=-50, vmax=50)
cbar=plt.colorbar()
cbar.set_label("SLA [m]", fontsize=labelsize)
plt.title("MEaSUREs sea level anomaly 2019-05-02", fontsize=titlesize)
plt.xlabel(f"Longitude [\N{DEGREE SIGN}]", fontsize=labelsize)
plt.ylabel(f"Latitude [\N{DEGREE SIGN}]", fontsize=labelsize)
plt.savefig(Path("figures", "presentation", "measures.png"))
plt.close()

plt.figure(figsize=(12,5), dpi=500)
plt.imshow(our.sla21[0]*100, origin="lower", extent=[-180,180,-80,80], cmap=cmc.vik, vmin=-50, vmax=50)
cbar=plt.colorbar()
cbar.set_label("SLA [m]", fontsize=labelsize)
plt.title("New product sea level anomaly 2019-05-02", fontsize=titlesize)
plt.xlabel(f"Longitude [\N{DEGREE SIGN}]", fontsize=labelsize)
plt.ylabel(f"Latitude [\N{DEGREE SIGN}]", fontsize=labelsize)
plt.savefig(Path("figures", "presentation", "our.png"))
plt.close()
