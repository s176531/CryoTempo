import xarray as xr
from pathlib import Path
from tqdm import tqdm
import numpy as np

PHASE = 21 # 1 or 21
MONTH = 8
BASEPATH = Path(f"D:/CryoTempo files/phase{PHASE}_arctic_all_years")
SAVEPATH = Path(f"data/yearly_average_phase{PHASE}")


def main():
    SAVEPATH.mkdir(parents=True, exist_ok=True)
    years = range(2011, 2024)
    average_sla, average_slar, average_slaf = [], [], []
    for year in tqdm(years, position=0):
        files = list(Path(BASEPATH).glob(f"combined_phase{PHASE}_arctic_all_years_{year}_{MONTH:02d}*.nc"))
        sla, slaf, slar = [],[],[]
        for file in tqdm(files, position=1):
            try:
                temp_data = xr.open_dataset(file)
            except ValueError:
                continue
            slar.append(np.nanmean(temp_data.sea_level_anomaly_raw))
            sla.append(np.nanmean(temp_data.sea_level_anomaly))
            slaf.append(np.nanmean(temp_data.sea_level_anomaly_filtered))
        average_sla.append(np.nanmean(sla))
        average_slar.append(np.nanmean(slar))
        average_slaf.append(np.nanmean(slaf))
    out_file = xr.Dataset(
        data_vars={
            "sea_level_anomaly_raw": average_slar,
            "sea_level_anomaly": average_sla,
            "sea_level_anomaly_filtered": average_slaf
            },
        coords={"time": [f"{year}-{MONTH:02d}" for year in years]}
        )
    out_file.to_netcdf(Path(SAVEPATH, f"yearly_averages_phase{PHASE}_{MONTH:02d}.nc"))

if __name__ == "__main__":
    main()
