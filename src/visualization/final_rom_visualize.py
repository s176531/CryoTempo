import numpy as np
import xarray as xr
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cmcrameri.cm as cmc
import cartopy.crs as ccrs
from tqdm import tqdm
from .. import load, get_month

POLE = "south" # "north" or "south"
PARAMETER = "_raw" # "" or "_filtered"
VLIM = None # None, int or float
CMAP = "jet"

def scatter_plot_SLA(data: xr.Dataset, parameter="", vlim=50, cmap=cmc.vik):
    save_folder = Path("figures", "rom_final", "scatter_plots", f"sea_level_anomaly{parameter}")
    save_folder.mkdir(parents=True, exist_ok=True)
    if POLE == "south":
        projection = ccrs.SouthPolarStereo()
        title_str = "Antarctic"
        figsize = (6,6)
    elif POLE == "north":
        projection = ccrs.NorthPolarStereo()
        title_str = "Arctic"
        figsize = (5,6.2)
    addition = ""
    if PARAMETER == "_filtered":
        addition = "filtered "

    for month in tqdm(np.arange(1,13)):
        im_data = get_month(data, month)
        fig=plt.figure(figsize=figsize, dpi=200, constrained_layout=True)
        ax = fig.add_subplot(1,1,1, projection=projection)
        if vlim:
            im=ax.scatter(im_data.longitude, im_data.latitude, c=im_data[f"sea_level_anomaly{parameter}"]*100, s=.001, cmap=cmap, transform=ccrs.Geodetic(), vmin=-vlim, vmax=vlim)
        else:
            im=ax.scatter(im_data.longitude, im_data.latitude, c=im_data[f"sea_level_anomaly{parameter}"]*100, s=.001, cmap=cmap, transform=ccrs.Geodetic())
        ax.coastlines()
        cbar = fig.colorbar(im, ax=ax, location="bottom", extend="both")
        cbar.set_label("SLA [cm]", fontsize=10)
        cbar.solids.set(alpha=1)
        ax.set_xlabel(f"Longitude [\N{DEGREE SIGN}]")
        ax.set_ylabel(f"Latitude [\N{DEGREE SIGN}]")
        ax.set_title(f"{title_str} {addition}Sea Level Anomaly 2019-{month:02d}")
        ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        plt.savefig(Path(save_folder, f"sea_level_anomaly{parameter}_{POLE}_{month}_jet.png"))
        plt.close()

    fig=plt.figure(figsize=figsize, dpi=200, constrained_layout=True)
    ax = fig.add_subplot(1,1,1, projection=projection)
    if vlim:
        im=ax.scatter(data.longitude, data.latitude, c=data[f"sea_level_anomaly{parameter}"]*100, s=.001, cmap=cmap, transform=ccrs.Geodetic(), vmin=-vlim, vmax=vlim)
    else:
        im=ax.scatter(data.longitude, data.latitude, c=data[f"sea_level_anomaly{parameter}"]*100, s=.001, cmap=cmap, transform=ccrs.Geodetic())
    ax.coastlines()
    cbar = fig.colorbar(im, ax=ax, location="bottom", extend="both")
    cbar.set_label("SLA [cm]", fontsize=10)
    cbar.solids.set(alpha=1)
    ax.set_xlabel(f"Longitude [\N{DEGREE SIGN}]")
    ax.set_ylabel(f"Latitude [\N{DEGREE SIGN}]")
    ax.set_title(f"{title_str} {addition}Sea Level Anomaly 2019")
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    plt.savefig(Path(save_folder, f"sea_level_anomaly{parameter}_{POLE}_jet.png"))
    plt.close()

def histogram_SLA(data: xr.Dataset, parameter="", vlim=50):
    save_folder = Path("figures", "rom_final", "histograms", f"sea_level_anomaly{parameter}")
    save_folder.mkdir(parents=True, exist_ok=True)
    if POLE == "north":
        title_str = "Arctic"
    elif POLE == "south":
        title_str = "Antarctic"
    addition = ""
    if PARAMETER == "_filtered":
        addition = "filtered "
    for month in tqdm(np.arange(1,13)):
        hist_data = get_month(data, month)
        plt.figure(figsize=(8,6), dpi=200)
        if vlim:
            plt.hist(hist_data[f"sea_level_anomaly{parameter}"]*100, bins=50, color="limegreen", range=(-vlim,vlim), rwidth=0.9)
        else:
            plt.hist(hist_data[f"sea_level_anomaly{parameter}"]*100, bins=50, color="limegreen", rwidth=0.9)
        mean = data[f"sea_level_anomaly{parameter}"].mean().item()*100
        plt.axvline(mean, ls="--", c="red", label=f"Mean: {mean:.4f} cm")
        handles, labels = plt.gca().get_legend_handles_labels()
        N_obs = mpatches.Patch(color="white", label=f"No. obs: {len(data[f'sea_level_anomaly{parameter}'])}")
        Std = mpatches.Patch(color="white", label=f"STD: {data[f'sea_level_anomaly{parameter}'].std().item()*100:.4f} cm")
        handles.extend([N_obs, Std])
        plt.legend(handles=handles)
        plt.xlabel("SLA [cm]")
        plt.title(f"{title_str} {addition}Sea Level Anomaly 2019-{month:02d}")
        plt.grid()
        plt.savefig(Path(save_folder, f"sea_level_anomaly{parameter}_{POLE}_{month}.png"))
        plt.close()
    

    plt.figure(figsize=(8,6), dpi=200)
    if vlim:
        plt.hist(data[f"sea_level_anomaly{parameter}"]*100, bins=50, color="limegreen", range=(-vlim,vlim), rwidth=0.9)
    else:
        plt.hist(data[f"sea_level_anomaly{parameter}"]*100, bins=50, color="limegreen", rwidth=0.9)
    mean = data[f"sea_level_anomaly{parameter}"].mean().item()*100
    plt.axvline(mean, ls="--", c="red", label=f"Mean: {mean:.4f} cm")
    handles, labels = plt.gca().get_legend_handles_labels()
    N_obs = mpatches.Patch(color="white", label=f"No. obs: {len(data[f'sea_level_anomaly{parameter}'])}")
    Std = mpatches.Patch(color="white", label=f"STD: {data[f'sea_level_anomaly{parameter}'].std().item()*100:.4f} cm")
    handles.extend([N_obs, Std])
    plt.legend(handles=handles)
    plt.xlabel("SLA [cm]")
    plt.title(f"{title_str} {addition}Sea Level Anomaly 2019")
    plt.grid()
    plt.savefig(Path(save_folder, f"sea_level_anomaly{parameter}_{POLE}_ALL.png"))
    plt.close()

### Dynamic Ocean Topography
def scatter_plot_DOT(data: xr.Dataset, parameter="", vlim=None, cmap=cmc.roma_r):
    save_folder = Path("figures", "rom_final", "scatter_plots", f"dynamic_ocean_topography{parameter}")
    save_folder.mkdir(parents=True, exist_ok=True)
    if POLE == "south":
        projection = ccrs.SouthPolarStereo()
        title_str = "Antarctic"
        figsize = (6,6)
    elif POLE == "north":
        projection = ccrs.NorthPolarStereo()
        title_str = "Arctic"
        figsize = (5,6.2)
    addition = ""
    if PARAMETER == "_filtered":
        addition = "filtered "

    for month in tqdm(np.arange(1,13)):
        im_data = get_month(data, month)
        fig=plt.figure(figsize=figsize, dpi=200, constrained_layout=True)
        ax = fig.add_subplot(1,1,1, projection=projection)
        if vlim:
            im=ax.scatter(im_data.longitude, im_data.latitude, c=im_data[f"dynamic_ocean_topography{parameter}"], s=.001, cmap=cmap, transform=ccrs.Geodetic(), vmin=-vlim, vmax=vlim)
        else:
            im=ax.scatter(im_data.longitude, im_data.latitude, c=im_data[f"dynamic_ocean_topography{parameter}"], s=.001, cmap=cmap, transform=ccrs.Geodetic())
        ax.coastlines()
        cbar = fig.colorbar(im, ax=ax, location="bottom", extend="both")
        cbar.set_label("DOT [m]", fontsize=10)
        cbar.solids.set(alpha=1)
        ax.set_xlabel(f"Longitude [\N{DEGREE SIGN}]")
        ax.set_ylabel(f"Latitude [\N{DEGREE SIGN}]")
        ax.set_title(f"{title_str} {addition}Dynamic Ocean Topography 2019-{month:02d}")
        ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        plt.savefig(Path(save_folder, f"dynamic_ocean_topography{parameter}_{POLE}_{month}.png"))
        plt.close()

    fig=plt.figure(figsize=figsize, dpi=200, constrained_layout=True)
    ax = fig.add_subplot(1,1,1, projection=projection)
    if vlim:
        im=ax.scatter(data.longitude, data.latitude, c=data[f"dynamic_ocean_topography{parameter}"], s=.001, cmap=cmap, transform=ccrs.Geodetic(), vmin=-vlim, vmax=vlim)
    else:
        im=ax.scatter(data.longitude, data.latitude, c=data[f"dynamic_ocean_topography{parameter}"], s=.001, cmap=cmap, transform=ccrs.Geodetic())
    ax.coastlines()
    cbar = fig.colorbar(im, ax=ax, location="bottom", extend="both")
    cbar.set_label("DOT [m]", fontsize=10)
    cbar.solids.set(alpha=1)
    ax.set_xlabel(f"Longitude [\N{DEGREE SIGN}]")
    ax.set_ylabel(f"Latitude [\N{DEGREE SIGN}]")
    ax.set_title(f"{title_str} {addition}Dynamic Ocean Topography 2019")
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    plt.savefig(Path(save_folder, f"dynamic_ocean_topography{parameter}_{POLE}.png"))
    plt.close()

def histogram_DOT(data: xr.Dataset, parameter="", vlim=None):
    save_folder = Path("figures", "rom_final", "histograms", f"dynamic_ocean_topography{parameter}")
    save_folder.mkdir(parents=True, exist_ok=True)
    if POLE == "north":
        title_str = "Arctic"
    elif POLE == "south":
        title_str = "Antarctic"
    addition = ""
    if PARAMETER == "_filtered":
        addition = "filtered "
    for month in tqdm(np.arange(1,13)):
        hist_data = get_month(data, month)
        plt.figure(figsize=(8,6), dpi=200)
        if vlim:
            plt.hist(hist_data[f"dynamic_ocean_topography{parameter}"], bins=50, color="limegreen", range=(-vlim,vlim), rwidth=0.9)
        else:
            plt.hist(hist_data[f"dynamic_ocean_topography{parameter}"], bins=50, color="limegreen", rwidth=0.9)
        mean = hist_data[f"dynamic_ocean_topography{parameter}"].mean().item()
        plt.axvline(mean, ls="--", c="red", label=f"Mean: {mean:.4f} m")
        handles, labels = plt.gca().get_legend_handles_labels()
        N_obs = mpatches.Patch(color="white", label=f"No. obs: {len(hist_data[f'dynamic_ocean_topography{parameter}'])}")
        Std = mpatches.Patch(color="white", label=f"STD: {hist_data[f'dynamic_ocean_topography{parameter}'].std().item():.4f} m")
        handles.extend([N_obs, Std])
        plt.legend(handles=handles)
        plt.xlabel("DOT [m]")
        plt.title(f"{title_str} {addition}Dynamic Ocean Topography 2019-{month:02d}")
        plt.grid()
        plt.savefig(Path(save_folder, f"dynamic_ocean_topography{parameter}_{POLE}_{month}.png"))
        plt.close()
    

    plt.figure(figsize=(8,6), dpi=200)
    if vlim:
        plt.hist(data[f"dynamic_ocean_topography{parameter}"], bins=50, color="limegreen", range=(-vlim,vlim), rwidth=0.9)
    else:
        plt.hist(data[f"dynamic_ocean_topography{parameter}"], bins=50, color="limegreen", rwidth=0.9)
    mean = data[f"dynamic_ocean_topography{parameter}"].mean().item()
    plt.axvline(mean, ls="--", c="red", label=f"Mean: {mean:.4f} m")
    handles, labels = plt.gca().get_legend_handles_labels()
    N_obs = mpatches.Patch(color="white", label=f"No. obs: {len(data[f'dynamic_ocean_topography{parameter}'])}")
    Std = mpatches.Patch(color="white", label=f"STD: {data[f'dynamic_ocean_topography{parameter}'].std().item():.4f} m")
    handles.extend([N_obs, Std])
    plt.legend(handles=handles)
    plt.xlabel("DOT [m]")
    plt.title(f"{title_str} {addition}Dynamic Ocean Topography 2019")
    plt.grid()
    plt.savefig(Path(save_folder, f"dynamic_ocean_topography{parameter}_{POLE}_ALL.png"))
    plt.close()

if __name__ == "__main__":
    north_data, south_data = load(Path("data", "po_tds_c_final"))

    if POLE == "north":
        # scatter_plot_DOT(north_data, PARAMETER, VLIM)
        # histogram_DOT(north_data, PARAMETER, VLIM)
        # scatter_plot_SLA(north_data, PARAMETER)
        histogram_SLA(north_data, PARAMETER)
    elif POLE == "south":
        # scatter_plot_DOT(south_data, PARAMETER, VLIM)
        # histogram_DOT(south_data, PARAMETER, VLIM)
        # scatter_plot_SLA(south_data, parameter=PARAMETER, cmap=CMAP)
        histogram_SLA(south_data, PARAMETER)
