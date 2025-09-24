import pandas as pd
import numpy as np
from typing import List, Optional
import itertools
import functools
import operator
import pdb

def greatest_abs_diff(
        dfs: dict[str, pd.DataFrame],
        metric_names: List[str] = 'rmse_weighted_l2',
        attributes: List[str] = 'all',
        iterate_over: Optional[List[str]] = ['model', 'variable', 'lead_time']
    ) -> dict[str, pd.DataFrame]:
    '''
    Get the greatest absolute difference in per-strata metric values for each
    attribute for each combination of the values for the columns specified in
    iterate_over. Returned as a dict from attribute (str) -> dataframe.
    '''
    # todo: validate list nature of args
    output = dict()
    if attributes == 'all':
        attributes = [k for k in dfs.keys() if k != 'baseline']

    for attribute in attributes:
        df = dfs[attribute]
        out_df = pd.DataFrame()
        iter_cols = [k for k in iterate_over if k in df.columns]
        iter_combos = list(itertools.product(*[df[k].unique() for k in iter_cols]))
        for iter_vals in iter_combos:
            conditions = [(df[col] == val) for col, val in zip(iter_cols, iter_vals)]
            pdb.set_trace()
            mask = functools.reduce(operator.and_, conditions)
            curr_df = df[mask]
            for metric in metric_names:
                pdb.set_trace()
                # todo: calc vals for the masked df, then append to out_df
        output[attribute] = out_df
            
    return output

def variance(
        
    ):
    pass
