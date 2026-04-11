import pandas as pd
import numpy as np
import FISIE_classes as FC
import math

STEP = 0.05
t_idx_mrg = 0 # will set later

suffix = "ar_0-05_"
base_file = "fisie_state_data_"


class FisieDataFrames(object):
    def __init__(self, base_file_name, strategy, time_col, num_files):
        self.base_file = base_file_name
        self.time_col = time_col
        self.num_files = num_files
        self.strategy = strategy

        # Build DataFrame structure
        self.tail_df = pd.DataFrame({"strategy": [], self.time_col: []})
        self.dataframes = dict()

        # Read dataframes
        for sim_idx in range(num_files):
            csvfile_name = f"{base_file_name}{sim_idx}.csv"

            # Read CSV and filter
            cols = ["strategy", self.time_col, "audit_type", "audit_result"]
            df = pd.read_csv(csvfile_name, usecols=cols)
            df = df.dropna()
            df = df[df["strategy"] == self.strategy] # filter by strategy
            df = df.sort_values(by=self.time_col).reset_index(drop=True)

            self.dataframes[sim_idx] = df  # future dataframes

            last_row = df.iloc[-1]
            lr_idx = len(df)-1
            new_row_tail = [self.strategy, last_row[self.time_col]]
            self.tail_df.loc[sim_idx] = new_row_tail


    def get_avg_ejection(self):
        mean = np.mean(self.tail_df[self.time_col])
        std = np.std(self.tail_df[self.time_col])
        min = np.min(self.tail_df[self.time_col])
        max = np.max(self.tail_df[self.time_col])
        print(f"Strategy: {self.strategy}, Mean: {mean}, Var: {std}, Min: {min}, Max: {max}")

    def get_oracle_audits(self):
        oracle_audits = []
        for idx, df in self.dataframes.items():
            df_o = df[df["audit_type"] == 1]
            oracle_audits.append(len(df_o))
        mean = np.mean(oracle_audits)
        min = np.min(oracle_audits)
        max = np.max(oracle_audits)
        var = np.var(oracle_audits)
        print(f"Strategy: {self.strategy}, Mean: {mean}, Var: {var}, Min: {min}, Max: {max}")

    def get_iot_audits(self):
        iot_audits = []
        pass_ratio = []
        for idx, df in self.dataframes.items():
            df_i = df[df["audit_type"] == 0]
            iot_audits.append(len(df_i))
            df_p = df_i[df_i["audit_result"] == 1]
            pr = len(df_p)/len(df_i)
            pass_ratio.append(pr)

        for v in [iot_audits, pass_ratio]:
            mean = np.mean(v)
            min = np.min(v)
            max = np.max(v)
            var = np.var(v)
            print(f"Strategy: {self.strategy}, Mean: {mean}, Var: {var}, Min: {min}, Max: {max}")



# Read DataFrames
base_file_name = f"{base_file}{suffix}"
time_col = "Time"
num_files = 50
for s in FC.Strategy:
    FDF = FisieDataFrames(base_file_name, s.name, time_col, num_files)
    FDF.get_avg_ejection()


