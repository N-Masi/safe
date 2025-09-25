import os
import pickle
import numpy as np
import pandas as pd
import geopandas as gpd
import pdb

models = ['graphcast', 'keisler', 'pangu', 'sphericalcnn', 'fuxi', 'neuralgcm']
variables = ['T850', 'Z500']
lead_times = [x for x in range(12, 241, 12)]
attributes = ['territory', 'subregion', 'income', 'landcover']

iclr_data_path = 'outputs/results_iclr.pkl'
if os.path.exists(iclr_data_path):
    with open(iclr_data_path, 'rb') as f:
        iclr_data = pickle.load(f)

output_latex = b''

for attr in attributes:
    output_latex += b'\n\n\\begin{table}\n\t\\caption{' + \
        bytes(attr, 'utf8') + \
        b'}\n\t\\label{' + \
        bytes(attr, 'utf8') + \
        b'-' + \
        b'-benchmark}\n\t\\scriptsize\n\t\\centering' + \
        b'\n\t\\begin{tabular}{lllllllll}\n\t\t\\\\ \\toprule' + \
        b'\n\t\t& & \\multicolumn{6}{c}{Model} \\\\' + \
        b'\n\t\t\\cmidrule(r){3-8}\n\t\tVariable & Lead time (h) & ' + \
        b'GraphCast & Keisler & Pangu-Weather & Spherical CNN & ' + \
        b'FuXi & NeuralGCM \\\\\n\t\t\\midrule'
    for variable in variables:
        for lead_time in lead_times:
            table_entry = b'\t\t' + bytes(variable, 'utf8') + b' & ' + bytes(str(lead_time), 'utf8') + b'h'
            vals = []
            for model in models:
                df = iclr_data[(iclr_data['variable']==variable) 
                    & (iclr_data['lead_time']==lead_time) 
                    & (iclr_data['model']==model)
                    & (iclr_data['attribute']==attr)
                ] 
                vals.append(df['gad_rmse_weighted_l2'].item()) # TODO: variance
            for val in vals:
                if val == min(vals):
                    table_entry += b' & \\textbf{' + bytes('{0:.4f}'.format(val), 'utf8') + b'}'
                else:
                    table_entry += b' & ' + bytes('{0:.4f}'.format(val), 'utf8')
            table_entry += b' \\\\'
            output_latex += b'\n' + table_entry
        if variable != variables[-1]: 
            output_latex += b'\n\t\t\\midrule'
    output_latex += b'\n\t\t\\bottomrule\n\t\\end{tabular}\n\\end{table}'  

# \begin{table}
#   \caption{Benchmark of models on the \textbf{income} attribute. Each cell contains the greatest absolute difference in per-strata RMSE of T850 or Z500 for a given model at a given lead time (rounded to the nearest ten-thousandth); lower is better. The RMSE difference for the best model per lead time per variable is in bold.}
#   \label{income-benchmark}
#   \scriptsize
#   \centering
#   \begin{tabular}{lllllllll}
#     \\ \toprule
#      & & \multicolumn{6}{c}{Model} \\
#      \cmidrule(r){3-8}
#      Variable & Lead time (h) & GraphCast & Keisler & Pangu-Weather & Spherical CNN & FuXi & NeuralGCM \\
#     \midrule
#     T850 & 12h & 0.0620 & 0.0778 & 0.0751 & 0.0774 & 0.0642 & \textbf{0.0542} \\
#     T850 & 72h & 0.1976 & 0.2746 & 0.2127 & 0.3468 & 0.1956 & \textbf{0.1735} \\
#     T850 & 240h & 2.0647 & 2.0616 & 1.9952 & 2.1247 & \textbf{1.5983} & 2.0702 \\
#     \midrule
#     Z500 & 12h & \textbf{0.8108} & 3.6642 & 1.6727 & 5.9048 & 1.5137 & 1.6832 \\
#     Z500 & 72h & 74.6146 & 84.2772 & 80.9830 & 104.9152 & 73.3257 & \textbf{68.6393} \\
#     Z500 & 240h & 577.7541 & 619.7738 & 600.2285 & 620.6610 & \textbf{483.7225} & 606.3814 \\
#     \bottomrule
#   \end{tabular}
# \end{table}

with open('outputs/iclr_tables_latex.txt', 'wb') as f:
    f.write(output_latex)
