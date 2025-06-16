# utilities/heart_rate.py

import pandas as pd
import os

class HeartRateProcessor:
    def __init__(self, csv_path, user_id):
        self.csv_path = csv_path
        self.user_id = user_id
        self.df_raw = None
        self.df_30min = None

    def load_data(self):
        self.df_raw = pd.read_csv(self.csv_path, parse_dates=['Time'])
        self.df_raw = self.df_raw[self.df_raw['Id'] == self.user_id]

    def calculate_rolling_avg(self):
        df = self.df_raw.copy()
        df = df.set_index('Time').resample('30min').mean().reset_index()
        df = df.rename(columns={'Value': 'avg_30_min'})
        df = df[['Time', 'avg_30_min']].dropna()
        self.df_30min = df

    @staticmethod
    def calculate_stress_score(avg_30_min):
        if avg_30_min < 65:
            return 0
        elif avg_30_min > 120:
            return 1
        else:
            return (avg_30_min - 65) / (120 - 65)

    def add_stress_score(self):
        self.df_30min['stress_score'] = self.df_30min['avg_30_min'].apply(self.calculate_stress_score)

    def get_processed_df(self):
        return self.df_30min

#Main execution
processor = HeartRateProcessor(
    csv_path=os.path.join(os.path.dirname(__file__), 'heart_rate_data', 'heartrate_seconds_merged.csv'),
    user_id=2022484408
)

processor.load_data()
processor.calculate_rolling_avg()
processor.add_stress_score()

df_result = processor.get_processed_df()
print(df_result)