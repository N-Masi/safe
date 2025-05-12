import sfear
import pandas as pd
import numpy as np

models = ['graphcast'] #['pangu', 'graphcast', 'fuxi']
resolution = '240x121' #'1440x721' TODO: implement 1440x721
lead_times = [np.timedelta64(x, 'h') for x in range(12, 241, 12)]
variables = ['T850', 'Z500']
era5 = sfear.data.era5.get_era5(res)
data = pd.DataFrame()
for model in models:
    preds = sfear.data.wb2.get_wb2_preds(model, resolution, lead_times)
    preds_gdf = sfear.metadata.collect_metadata(preds, lon_dim='longitude', lat_dim='latitude')
    metrics = sfear.metadata.metacategory_climate_metrics(preds_gdf, era5, variables=variables, categories='all')
    # TODO: append model_name to metrics as a new column
    # TODO: append metrics to data
with open('outputs/wb2_1440x721.pkl', 'wb') as f:
    pickle.dump(data, f)
# TODO: call sfear.viz (put this in one of the loops)
