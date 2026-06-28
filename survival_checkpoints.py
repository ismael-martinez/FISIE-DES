import matplotlib.pyplot as plt
import pandas as pd
import FISIE_classes as FC

ratio = '0-025'
csvfile_name = f"fisie_merged_ar_{ratio}_fog_count.csv"
df = pd.read_csv(csvfile_name)

rep_df = pd.read_csv(f"fisie_merged_ar_{ratio}_avg_reputation.csv")
pr_df = pd.read_csv(f"fisie_merged_ar_{ratio}_avg_profit.csv")

time_col = "Time"
val_df = pd.DataFrame({time_col: [], "strategy": [], "percent":[], "reputation":[], "rep_idx":[], "profit":[], "pr_idx":[]})#, "reliability":[], "rel_idx":[]})
percentile_step = 0.25
i = 1 # start
j = 1./percentile_step # end non-inclusive (< j)

for s in FC.Strategy:
    s_df = df[df["strategy"] == s.name]  # filter by strategy
    total_fog_count = s_df['fog_count'].max()
    percentile = (1-percentile_step)
    count_steps = total_fog_count*percentile
    for index, row in s_df.iterrows():
        if row['fog_count'] <= count_steps and i < j:
            time = row['Time']
            rep_df_s = rep_df.loc[(rep_df['strategy']==s.name)]
            rep_df_s = rep_df_s.reset_index(drop=True)
            rep_row = rep_df_s.loc[(rep_df_s['Time']==time), 'avg_reputation']
            rep = (rep_row.iloc[0], rep_row.index[0])

            pr_df_s = pr_df.loc[(pr_df['strategy']==s.name)]
            pr_df_s = pr_df_s.reset_index(drop=True)
            pr_row = pr_df_s.loc[(pr_df_s['Time'] == time), "avg_profit"]
            pr = (pr_row.iloc[0], pr_row.index[0])

            # rel_df_s = rel_df.loc[(rel_df['strategy']==s.name)]
            # rel_df_s = rel_df_s.reset_index(drop=True)
            # rel_row = rel_df_s.loc[(rel_df_s['Time']== time), "avg_reliability"]
            # rel = (rel_row.iloc[0], rel_row.index[0])

            val_df.loc[len(val_df)] = [row['Time'], row['strategy'], percentile, rep[0], rep[1], pr[0], pr[1]]
            percentile -= percentile_step
            count_steps = total_fog_count * percentile
            i += 1
    i = 1 # reset for next strategy
val_df = val_df.sort_values(by=time_col).reset_index(drop=True)
print(val_df.head())




new_csvfile_name = f"fisie_survival_points_{ratio}.csv"
val_df.to_csv(new_csvfile_name, index=False)