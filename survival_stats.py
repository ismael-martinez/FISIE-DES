import matplotlib.pyplot as plt
import pandas as pd
import FISIE_classes as FC
import numpy as np

ratio =  '0-05'
suffix = f"ar_{ratio}_"
base_file = "fisie_state_data_"

fog_total = 1000
steps = 0.25
num_files = 50

quartile_arrays = dict()
for s in FC.Strategy:
    quartile_arrays[s.name] = dict()
    for q in range(4):
        quartile_arrays[s.name][q*steps] = []


for f in range(num_files):
    file_name = f"{base_file}{suffix}{f}.csv"
    df = pd.read_csv(file_name)
    for s in FC.Strategy:
        s_df = df.loc[df['strategy']==s.name, ['Time', 'audit_cycle', 'fog_count']]
        for q in range(3,-1, -1):
            s_df_q = s_df.loc[s_df['fog_count']==q*steps*fog_total, 'audit_cycle']
            quartile_arrays[s.name][q*steps].append(s_df_q.iloc[0])

new_df = pd.DataFrame({'strategy':[], 'quartile':[], 'cycle_mean':[], 'cycle_sd':[]})
for s in FC.Strategy:
    for q in range(4):
        q_array = quartile_arrays[s.name][q*steps]
        row = [s.name, q*steps, np.mean(q_array), np.std(q_array)]
        new_df.loc[len(new_df)] = row

new_csvfile_name = f"fisie_survival_checkpoints_{ratio}.csv"
new_df.to_csv(new_csvfile_name, index=False)