import pandas as pd


class Streamer:
    def __init__(self, filename, req_cols=None):
        self.df, self.req_df = self.read_data(filename,
                                              req_cols=req_cols)
        self.device_ids = self.req_df["Device name"].unique()

    def read_data(self, filename, req_cols=None):
        df = pd.read_csv(filename)
        df = df.reset_index()
        df.iloc[:, :] = df.iloc[:, :].shift(axis=1)
        df = df.drop(["index"], axis=1)
        if isinstance(req_cols, str):
            req_cols = req_cols.strip().split(",")
        req_df = df[req_cols]
        self.device_ids = req_df["Device name"].unique()
        return df, req_df

    def stream(self):
        for i in range(len(self.req_df)):
            yield self.req_df.iloc[i, :]
