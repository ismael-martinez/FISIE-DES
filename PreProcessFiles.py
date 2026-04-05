import pandas as pd

class DataFrames(object):
    def __init__(self, base_file_name, time_col, val_col, num_files):
        self.base_file = base_file_name
        self.time_col = time_col
        self.val_col = val_col
        self.num_files = num_files
        self.dataframes = dict()
        self.tail_df = pd.DataFrame({"idx":[], time_col:[], val_col: []})

        # Read dataframes
        for sim_idx in range(num_files):
            csvfile_name = f"{base_file_name}{sim_idx}.csv"
            df = pd.read_csv(csvfile_name, usecols=[time_col, val_col])
            df = df[df[self.val_col].notna()]
            self.dataframes[sim_idx] = df
            # Adding last row
            last_row = df.iloc[-1]
            lr_idx = len(df)
            new_row = [lr_idx, last_row[self.time_col], last_row[self.val_col]]
            self.tail_df.loc[sim_idx] = new_row
        print(self.tail_df.head())




value = "avg_reputation"
time = "Time"
base_file = "fisie_state_data_"
num_files = 5

DF = DataFrames(base_file, time, value, num_files)