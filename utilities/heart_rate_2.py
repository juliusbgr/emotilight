import pandas as pd
import os
from datetime import datetime

class HeartRateProcessor:
    def __init__(self, csv_path_hr, csv_path_state, user_id):
        self.csv_path_hr = csv_path_hr
        self.csv_path_state = csv_path_state
        self.user_id = user_id
        self.df_raw = None
        self.df_30min = None
        self.state_mapping = None

    def load_data(self):
        self.df_raw = pd.read_csv(self.csv_path_hr, parse_dates=['Time'])
        self.df_raw = self.df_raw[self.df_raw['Id'] == self.user_id]

    def calculate_rolling_avg(self):
        df = self.df_raw.copy()
        df = df.set_index('Time').resample('30min').mean().reset_index()
        df = df.rename(columns={'Value': 'avg_30_min'})
        df = df[['Time', 'avg_30_min']].dropna()
        df['only_time'] = df['Time'].dt.time
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
        self.df_30min['stress_score_hr'] = self.df_30min['avg_30_min'].apply(self.calculate_stress_score)

    def load_state_mapping(self):
        # the file with states
        df_state = pd.read_csv(self.csv_path_state)
        df_state = df_state.rename(columns={'Heart Rate (bpm)': 'HeartRate', 'State': 'State'})
        
    
        
        # Mapping for staates
        state_weights = {
            'Very calm': 0.0,
            'Calm': 0.1,
            'Normal': 0.3,
            'Slightly active': 0.5,
            'Active': 0.7,
            'Very active': 0.9,
            'Highly active': 1.0
        }

        # Mapping sress score for each state
        df_state['stress_score_state'] = df_state['State'].map(state_weights)
        self.state_mapping = df_state

    def merge_state_stress(self):
        # round the calculaated aaverage
        self.df_30min['avg_hr_rounded'] = self.df_30min['avg_30_min'].round().astype(int)

        # Merge with maapping
        self.df_30min = self.df_30min.merge(
            self.state_mapping[['HeartRate', 'stress_score_state']],
            left_on='avg_hr_rounded',
            right_on='HeartRate',
            how='left'
        )

        # combined score
        self.df_30min['stress_score_combined'] = self.df_30min[['stress_score_hr', 'stress_score_state']].mean(axis=1)

        self.df_30min = self.df_30min.drop(columns=['avg_hr_rounded', 'HeartRate'])

    def get_processed_df(self):
        return self.df_30min

# Main execution
def get_wearable_stress_score(time):
    processor = HeartRateProcessor(
        csv_path_hr=os.path.join(os.path.dirname(__file__), 'heart_rate_data', 'heartrate_seconds_2022484408_09April.csv'),
        csv_path_state=os.path.join(os.path.dirname(__file__), 'heart_rate_data', 'heart_rate_states.csv'),
        user_id=2022484408
    )

    processor.load_data()
    processor.calculate_rolling_avg()
    processor.add_stress_score()
    processor.load_state_mapping()
    processor.merge_state_stress()

    df_result = processor.get_processed_df().copy().sort_values(by='Time').reset_index(drop=True)
    input_time = datetime.strptime(time, "%H:%M").time()
    
    # Filter rows ending at or before input time
    filtered = df_result[df_result['only_time'] <= input_time]

    if filtered.empty:
        return None

    latest_row = filtered.iloc[-1]
    print(latest_row)
    return latest_row['stress_score_combined']

get_wearable_stress_score('13:00')