### Commented Lines that shift axes as written csv files dont have any discrepancy

import pandas as pd


class Streamer:
    def __init__(self, filename, req_cols=None):
        self.df, self.req_df = self.read_data(filename,
                                              req_cols=req_cols)
        self.device_ids = self.req_df["Device name"].unique()

    def read_data(self, filename, req_cols=None):
        df = pd.read_csv(filename)
        df = df.reset_index()
        #df.iloc[:, :] = df.iloc[:, :].shift(axis=1)
        #df = df.drop(["index"], axis=1)
        if isinstance(req_cols, str):
            req_cols = req_cols.strip().split(",")
        req_df = df[req_cols]
        self.device_ids = req_df["Device name"].unique()
        return df, req_df

    def stream(self):
        for i in range(len(self.req_df))[:]:
            yield self.req_df.iloc[i, :]

'''import pandas as pd

class Streamer:
    def __init__(self, filename, req_cols=None):
        self.req_df = self.read_data(filename, req_cols=req_cols)
        self.device_ids = self.req_df["Device name"].unique()

    def read_data(self, filename, req_cols=None):
        df = pd.read_csv(filename)
        df['Time'] = pd.to_datetime(df['Time'])
        df.set_index('Time', inplace=True)  # Move this line before accessing columns
        print("Columns in DataFrame:", df.columns)  # Print column names
        print("First few rows of DataFrame:", df.head())
        if isinstance(req_cols, str):
            req_cols = req_cols.strip().split(",")
        req_df = df[req_cols]
        return req_df

    def resample_data(self, freq='50L'):
        resampled_dfs = []
        for device_id in self.device_ids:
            device_df = self.req_df[self.req_df['Device name'] == device_id]
            resampled_df = device_df.resample(freq).first().fillna(method='ffill')
            resampled_dfs.append(resampled_df)
        self.req_df = pd.concat(resampled_dfs)

    def calculate_difference(self):
        for col in self.req_df.columns:
            if col.startswith('Acceleration'):
                self.req_df[col + '_diff'] = self.req_df[col].diff()

    def stream(self):
        for index, row in self.req_df.iterrows():
            yield row
'''