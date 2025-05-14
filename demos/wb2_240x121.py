import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import safe.data.climate.era5
import safe.data.climate.wb2
import safe.metrics.losses
import safe.metrics.errors
import pandas as pd
import numpy as np
import pickle
import time
import pdb

start = time.time()

models = ['pangu', 'sphericalcnn', 'fuxi', 'neuralgcm'] #'graphcast', 'keisler', 
resolution = '240x121' #'1440x721' TODO: implement 1440x721
lead_times = [np.timedelta64(x, 'h') for x in range(12, 241, 12)]
variables = ['T850', 'Z500'] # TODO: pass these to get_era5 and get_wb2_preds to have user-defined variables
era5 = safe.data.climate.era5.get_era5(resolution)
for model_name in models:
    model_start = time.time()
    preds = safe.data.climate.wb2.get_wb2_preds(model_name, resolution, lead_times)
    loss_gdf = safe.metrics.losses.climate_weighted_l2(
        data=preds, 
        ground_truth=era5, 
        lon_dim='longitude', 
        lat_dim='latitude',
        lead_time_dim='prediction_timedelta',
        reduction_dims=['time'],
        use_polygons=True,
        polygon_edge_in_degrees=1.5,
    )
    # loss_gdf.to_csv(f'outputs/weighted_l2_{model_name}_{resolution}.csv', index=False)
    # print(f'Execution time to get weighted l2: {time.time() - model_start}')
    metrics = safe.metrics.errors.stratified_rmse(
        loss_gdf,
        loss_metrics=['weighted_l2'],
        strata_groups='all',
        added_cols={'model': model_name}
    )
    # print(f'Execution time to get RMSEs: {time.time() - model_start}')
    with open(f'outputs/metrics_{model_name}_{resolution}.pkl', 'wb') as f:
        pickle.dump(metrics, f)

# TODO: call safe.viz (put this in one of the loops)

print(f'Time to complete script: {time.time() - start}')
print(f'Models: {models}')
print(f'Resolution: {resolution}')
print(f'Lead times: {lead_times}')
