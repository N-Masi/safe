import plotly.express as px
import os
import pickle
import numpy as np
import pandas as pd
import geopandas as gpd

# define constants
models = ['graphcast', 'keisler', 'pangu', 'sphericalcnn', 'fuxi', 'neuralgcm']
newnames = {'graphcast':'GraphCast', 'keisler': 'Keisler (2022)', 'pangu': 'Pangu-Weather', 'sphericalcnn': 'Spherical CNN', 'fuxi': 'FuXi', 'neuralgcm': 'NeuralGCM'}
lead_times = [x for x in range(12, 241, 12)]
attributes = ['territory', 'subregion', 'income', 'landcover']

# collate all model data into unified dataframes
iclr_data_path = 'outputs/results_iclr.pkl'
if not os.path.exists(iclr_data_path):
    print('regathering data')
    iclr_data = pd.DataFrame()
    for attr in attributes:
        for model in models:
            with open(f'outputs/results_{model}_iclr.pkl', 'rb') as f:
                model_dict = pickle.load(f)
            model_df = model_dict[attr]
            model_df['attribute'] = attr
            iclr_data = pd.concat([iclr_data, model_df], ignore_index=True)
    with open(iclr_data_path, 'wb') as f:
        pickle.dump(iclr_data, f)
else:
    with open(iclr_data_path, 'rb') as f:
        iclr_data = pickle.load(f)

# plot Figure 2
fig_gad = px.line(
    iclr_data,
    x='lead_time',
    y='gad_rmse_weighted_l2',
    color='model',
    symbol='model',
    symbol_sequence=['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up'],
    facet_col='attribute',
    facet_col_spacing=0.04,
    facet_row='variable',
    facet_row_spacing=0.04,
    labels={
        'lead_time': 'lead time (hours)',
        'gad_rmse_weighted_l2': 'Greatest Absolute Difference in per-strata RMSE'
    }
)
fig_gad.for_each_trace(lambda t: t.update(name = newnames[t.name],
    legendgroup = newnames[t.name],
    hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
    )
)
fig_gad.update_xaxes(tickmode = 'array', tickvals = lead_times, showticklabels = True, tickangle=-45, tickfont_size=8, title_font_size=10)
fig_gad.update_yaxes(matches=None, showticklabels=True)
fig_gad.show()
fig_gad.write_image('outputs/viz/iclr/rmse_diff.pdf', width=1200, height=800, scale=4)

# plot Figure 3
fig_var = px.line(
    iclr_data,
    x='lead_time',
    y='variance_rmse_weighted_l2',
    color='model',
    symbol='model',
    symbol_sequence=['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up'],
    facet_col='attribute',
    facet_col_spacing=0.04,
    facet_row='variable',
    facet_row_spacing=0.04,
    labels={
        'lead_time': 'lead time (hours)',
        'variance_rmse_weighted_l2': 'Variance in per-strata RMSE'
    }
)
fig_var.for_each_trace(lambda t: t.update(name = newnames[t.name],
    legendgroup = newnames[t.name],
    hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
    )
)
fig_var.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].capitalize()))
fig_var.update_xaxes(tickmode = 'array', tickvals = lead_times, showticklabels = True, tickangle=-45, tickfont_size=8, title_font_size=10)
fig_var.update_yaxes(matches=None, showticklabels=True)
fig_var.show()
fig_var.write_image('outputs/viz/iclr/rmse_var.pdf', width=1200, height=800, scale=4)

# Figure X
# inc_data = iclr_data[iclr_data['attribute']=='income']
# fig_inc = px.line(
#     inc_data,
#     x='lead_time',
#     y='gad_rmse_weighted_l2',
#     color='income',
#     symbol='income',
#     facet_col='model',
#     facet_col_spacing=0.04,
#     facet_row='variable',
#     facet_row_spacing=0.04,
#     labels={
#         'lead_time': 'lead time (hours)'
#     },
#     category_orders={
#         'income': ['High-income Countries', 'Upper-middle-income Countries', 'Lower-middle-income Countries', 'Low-income Countries', 'Baseline (all gridpoints)']
#     }
# )
# fig_inc.for_each_trace(lambda t: t.update(name = newnames[t.name],
#     legendgroup = newnames[t.name],
#     hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
#     )
# )
# fig_inc.update_xaxes(tickmode = 'array', tickvals = lead_times, showticklabels = True, tickangle=-45, tickfont_size=8, title_font_size=10)
# fig_inc.show()
# fig_inc.write_image('outputs/viz/iclr/rmse_diff_income.pdf', width=1200, height=800, scale=4)
