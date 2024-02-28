import xarray as xr
from pathlib import Path
from tqdm import tqdm
import numpy as np

PHASE = 1 # 1 or 21
MONTHS = [1, 2, 3, 6, 7, 8]
BASEPATH = Path(f"data/save_folder_Beaufort_phase{PHASE}")
SAVEPATH = Path(f"data/yearly_average_Beaufort_phase{PHASE}")
SAVEPATH.mkdir(parents=True, exist_ok=True)

def main():
    for month in MONTHS:
        # if Path(SAVEPATH, f"yearly_averages_phase{PHASE}_{month:02d}.nc").exists():
        #     continue
        average_sla, average_slar, average_slaf, years = [], [], [], []
        n_points = 0
        for file in tqdm(list(BASEPATH.glob("*.nc"))):
            data = xr.open_dataset(file)
            year=file.stem[-4:]
            years.append(year)
            min_time = np.datetime64(f"{year}-{month:02d}-01")
            max_time = np.datetime64(f"{year}-{month+1:02d}-01") # doesnt work with december
            data_month = data.isel(time=(data.time < max_time) & (data.time >= min_time))
            slar = np.nanmean(np.multiply(data_month.sea_level_anomaly_raw.values,np.cos(data_month.latitude.values*np.pi/180)))
            sla = np.nanmean(np.multiply(data_month.sea_level_anomaly, np.cos(data_month.latitude*np.pi/180)))
            slaf = np.nanmean(np.multiply(data_month.sea_level_anomaly_filtered, np.cos(data_month.latitude*np.pi/180)))

            average_slar.append(slar)
            average_sla.append(sla)
            average_slaf.append(slaf)
            n_points += len(data_month.time)

        out_file = xr.Dataset(
            data_vars={
                "sea_level_anomaly_raw": average_slar,
                "sea_level_anomaly": average_sla,
                "sea_level_anomaly_filtered": average_slaf
                },
            coords={"time": [f"{yr}-{month:02d}" for yr in years]},
            attrs={"N_points": n_points}
            )
        out_file.to_netcdf(Path(SAVEPATH, f"yearly_averages_phase{PHASE}_{month:02d}.nc"))

if __name__ == "__main__":
    main()
