import plotly.express as px
import os
import pickle
import numpy as np
import pandas as pd
import geopandas as gpd
import safe_earth.metrics.fairness as fairness
from safe_earth.utils.stats import filter_outliers
from typing import Union, List, Optional, Dict

def graph_model_fairness(
        model_fairness_dictionary_filepaths: List[str],
        y_variable: str,
        model_display_names: Optional[Dict[str, str]] = None, # mapping of new display names for models
        y_variable_display_name: Optional[str] = None, # mapping of new display names for y-axis variable
        attributes: List[str] = ['territory', 'subregion', 'income', 'landcover'],
        lead_times: List[int] = [x for x in range(12, 241, 12)], # default is every 12 hours up to 10 days
        save_path: Optional[str] = None, # if defined, the figure will be saved to disk
        show: bool = True, # whether to display the figure as soon as generated
    ):

    # collect data for all models into one dataframe
    data = pd.DataFrame()
    for attr in attributes:
        for path in model_fairness_dictionary_filepaths:
            with open(path, 'rb') as f:
                model_dict = pickle.load(f)
            model_df = model_dict[attr]
            model_df['attribute'] = attr
            data = pd.concat([data, model_df], ignore_index=True)

    # y-axis label mapping
    if not y_variable_display_name:
        y_variable_display_name = y_variable

    # basic figure
    fig = px.line(
        data,
        x='lead_time',
        y=y_variable,
        color='model',
        symbol='model',
        symbol_sequence=['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up'],
        facet_col='attribute',
        facet_col_spacing=0.04,
        facet_row='variable',
        facet_row_spacing=0.04,
        labels={
            'lead_time': 'lead time (hours)',
            y_variable: y_variable_display_name
        }
    )

    # apply display names for models
    fig.for_each_trace(lambda t: t.update(name = model_display_names[t.name],
        legendgroup = model_display_names[t.name],
        hovertemplate = t.hovertemplate.replace(t.name, model_display_names[t.name])
        )
    )

    # format axes and annotations
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].capitalize()))
    fig.update_xaxes(tickmode = 'array', tickvals = lead_times, showticklabels = True, tickangle=-90, tickfont_size=8, title_font_size=10)
    fig.update_yaxes(matches=None, showticklabels=True)

    if save_path:
        fig.write_image(save_path, width=1200, height=800, scale=4)
    
    if show:
        fig.show()
