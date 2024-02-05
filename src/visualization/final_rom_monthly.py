import numpy as np
import xarray as xr
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cmcrameri.cm as cmc
import cartopy.crs as ccrs
from tqdm import tqdm
# from fastkml import kml
# from lxml import etree
from pykml import parser

def monthly_comparison():
    """"""
    folder = Path("data", "po_tds_c_final")
    tide_gauge = np.loadtxt(Path(folder, Path("psmsl_puerto_soberania", "data.txt")), delimiter=";")
    cryotempo = xr.open_dataset(Path(folder, "monthly_averages.nc"))

    tide_gauge_SLA = tide_gauge[:, 1]/1000
    tide_gauge_SLA[10] = np.nan

    data_type = "sea_level_anomaly_raw"

    offset = np.nanmean(tide_gauge_SLA) - cryotempo[data_type].mean()
    tide_gauge_SLA_corr = tide_gauge_SLA - offset.item()

    time = np.arange(1,13)+(2019-1970)*12-1
    time = time.astype("datetime64[M]")
    plt.figure(figsize=(12,6), dpi=100)
    plt.plot(time, tide_gauge_SLA_corr, 'o-', label="Puerto Soberania")
    plt.plot(time, cryotempo[data_type]-0.05, 'o-', label="CryoTEMPO raw")
    plt.plot(time, cryotempo["sea_level_anomaly"]-0.05, 'o-', label="CryoTEMPO")
    plt.plot(time, cryotempo["sea_level_anomaly_filtered"]-0.05, 'o-', label="CryoTEMPO filtered")
    plt.title("Monthly average of Puerto Soberania tide gauge station vs. CryoTempo")
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel("SLA [m]")
    plt.legend()
    plt.show()

def get_month(data: xr.DataArray, month: int):
    """Return data for chosen month"""
    if (month < 1) | (month > 12):
        raise ValueError("month should be in the interval [1, 12]")
    months = data.time.values.astype('datetime64[M]').astype(int) % 12 + 1
    return data.isel(time=months==month)

def syowa():
    folder = Path("data", "po_tds_c_final")
    tide_gauge = xr.open_dataset(Path(folder, "syowa.nc"))
    cryotempo = xr.open_dataset(Path(folder, "monthly_averages_syowa.nc"))

    tg_average = []
    for month in tqdm(np.arange(1,13)):
        monthly_data = get_month(tide_gauge, month)
        monthly_average = np.nanmean(monthly_data.sea_level.values[0])
        tg_average.append(monthly_average)
    tide_gauge_SLA = np.array(tg_average)/1000

    data_type = "sea_level_anomaly_raw"

    offset = np.mean(tide_gauge_SLA) - cryotempo[data_type].mean()
    tide_gauge_SLA_corr = tide_gauge_SLA - offset.item()

    time = np.arange(1,13)+(2019-1970)*12-1
    time = time.astype("datetime64[M]")
    plt.figure(figsize=(12,6), dpi=100)
    plt.plot(time, tide_gauge_SLA_corr, 'o-', label="Syowa")
    plt.plot(time, cryotempo[data_type], 'o-', label="CryoTEMPO raw")
    plt.plot(time, cryotempo["sea_level_anomaly"], 'o-', label="CryoTEMPO")
    plt.plot(time, cryotempo["sea_level_anomaly_filtered"], 'o-', label="CryoTEMPO filtered")
    plt.title("Monthly average of Syowa tide gauge station vs. CryoTempo")
    plt.grid()
    plt.xlabel("Month")
    plt.ylabel("SLA [m]")
    plt.legend()
    plt.show()




if __name__ == "__main__":
    monthly_comparison()
    syowa()
