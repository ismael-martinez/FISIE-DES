import pandas as pd
import numpy as np
import FISIE_classes as FC
import math

STEP = 0.05
t_idx_mrg = 0 # will set later

suffix = "ar_0-05_"
base_file = "fisie_state_data_"


class FisieDataFrames(object):
    def __init__(self, base_file_name, strategy, time_col, val_col, num_files):
        self.base_file = base_file_name
        self.time_col = time_col
        self.val_col = val_col
        self.num_files = num_files
        self.strategy = strategy

        # Build DataFrame structure
        self.tail_df = pd.DataFrame({"idx": [], "strategy": [], self.time_col: [], self.val_col: []})
        self.dataframes = dict()

        # Read dataframes
        for sim_idx in range(num_files):
            self.dataframes[sim_idx] = pd.DataFrame({self.time_col:[], "strategy": [], self.val_col: []})
            csvfile_name = f"{base_file_name}{sim_idx}.csv"

            # Read CSV and filter
            cols = [self.time_col, "strategy", self.val_col]
            df = pd.read_csv(csvfile_name, usecols=cols)
            df = df.dropna()
            df = df[df["strategy"] == self.strategy] # filter by strategy
            df = df.sort_values(by=self.time_col).reset_index(drop=True)
            self.dataframes[sim_idx] = df  # future dataframes

            last_row = df.iloc[-1]
            lr_idx = len(df)-1
            new_row_tail = [lr_idx, self.strategy, last_row[self.time_col], last_row[self.val_col]]
            self.tail_df.loc[sim_idx] = new_row_tail

        #print(self.tail_df.head())




def create_new_df(time_col, strategy, val_col, num_files):

    # Read DataFrame
    file = f"{base_file}{suffix}"
    DF = FisieDataFrames(file, strategy, time_col, val_col, num_files)

    # Build new DataFrame
    n_idx = 0
    merged_df = pd.DataFrame({time_col: [], "strategy":[], val_col: []})

    # Find maximum timestamp from tail_df - becomes starting point for merged_df
    t_idx_mrg = DF.tail_df[time_col].max()
    t_idx_mrg = math.ceil(t_idx_mrg*20)/20 # Round up to nearest 0.05

    while True:
        # Mean value
        avg_val = DF.tail_df[val_col].mean()
        # Append to new df
        new_row = [t_idx_mrg, strategy, avg_val]
        merged_df.loc[n_idx] = new_row
        n_idx += 1
        t_idx_mrg -= STEP
        t_idx_mrg = round(t_idx_mrg, 2)

        # adjust tail_df
        if t_idx_mrg >= 0:
            for t_idx, row in DF.tail_df.iterrows():
                n = 0
                t = DF.dataframes[t_idx].loc[row['idx'] - n][time_col]
                while t > t_idx_mrg and t_idx_mrg >= 0:
                    n += 1
                    t = DF.dataframes[t_idx].loc[row['idx'] - n][time_col]
                prev_id = row['idx'] - n
                data_row = DF.dataframes[t_idx].loc[prev_id]
                id_row = pd.Series({"idx": prev_id})
                full_row = pd.concat([data_row, id_row])
                DF.tail_df.loc[t_idx] = full_row

        else:
            merged_df = merged_df.sort_values(by=time_col).reset_index(drop=True)
            print(merged_df.head())
            return merged_df




# Read DataFrames
values = ["avg_reputation", "avg_profit", "fog_count"]
time_col = "Time"
num_files = 50
for v in values:
    val_df = pd.DataFrame({time_col:[], "strategy": [], v:[]})
    for s in FC.Strategy:
        s_df = create_new_df(time_col, s.name, v, num_files)
        val_df = pd.concat([val_df, s_df])
    filename = f"fisie_merged_{suffix}{v}.csv"
    val_df = val_df.sort_values(by=time_col).reset_index(drop=True)
    val_df.to_csv(filename, index=False)


