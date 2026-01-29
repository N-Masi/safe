import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import safe_earth
from safe_earth.data.climate.era5 import ERA5Var
import safe_earth.metrics.fairness as fairness
import pandas as pd
import numpy as np
import pickle
from safe_earth.viz import graph_model_fairness

def generate_data():
    models = ['neuralgcm', 'neuralgcm-ens-mean']
    resolution = '240x121'
    lead_times = [np.timedelta64(x, 'h') for x in range(12, 241, 12)]
    variables = [ERA5Var('temperature', 850, 'T850'), ERA5Var('geopotential', 500, 'Z500')]
    era5 = safe_earth.data.climate.era5.get_era5(resolution, variables=variables)

    for model in models:
        preds = safe_earth.data.climate.wb2.get_wb2_preds(model, resolution, lead_times, variables=variables)

        loss_gdf = safe_earth.metrics.losses.climate_weighted_l2(
            data=preds, 
            ground_truth=era5, 
            lon_dim='longitude', 
            lat_dim='latitude',
            lead_time_dim='prediction_timedelta'
        )

        strata_metrics = safe_earth.metrics.errors.stratified_rmse(
            loss_gdf,
            loss_metrics=['weighted_l2'],
            attributes='all',
            added_cols={'model': model}
        )

        with open(f'outputs/results_{model}_errors.pkl', 'wb') as f:
            pickle.dump(strata_metrics, f)

        fairness_metrics = fairness.measure_fairness(strata_metrics, funcs=[fairness.greatest_abs_diff, fairness.variance])

        with open(f'outputs/results_{model}_fairness_metrics.pkl', 'wb') as f:
            pickle.dump(fairness_metrics, f)

def plot():

    # set up paths
    output_dir = 'outputs/'
    viz_dir = output_dir+'viz/icml/'
    neuralgcm_pkl = output_dir+'results_neuralgcm_fairness_metrics.pkl'
    neuralgcm_ens_pkl = output_dir+'results_neuralgcm-ens-mean_fairness_metrics.pkl'

    # get common arguments
    dictionary_filepaths = [neuralgcm_pkl, neuralgcm_ens_pkl]
    display_names = {'neuralgcm': 'NeuralGCM', 'neuralgcm-ens-mean': 'NeuralGCM Ensemble Mean'}
    
    graph_model_fairness(
        model_fairness_dictionary_filepaths = dictionary_filepaths,
        y_variable = 'gad_rmse_weighted_l2',
        y_variable_display_name = 'Max Difference in Per-Strata RMSE',
        model_display_names = display_names,
        save_path = viz_dir+'fairness_neuralgcm_ens_gad.pdf'
    )

    graph_model_fairness(
        model_fairness_dictionary_filepaths = dictionary_filepaths,
        y_variable = 'variance_rmse_weighted_l2',
        y_variable_display_name = 'Variance in Per-Strata RMSE',
        model_display_names = display_names,
        save_path = viz_dir+'fairness_neuralgcm_ens_variance.pdf'
    )

if __name__ == '__main__':
    generate_data()
    plot()