import pandas as pd

df = pd.read_csv('utilities\heart_rate_data\heartrate_seconds_merged.csv', parse_dates=['Time'])
df_user1 = df[df['Id'] == 2022484408]
# df_user1.loc[:,'Time'] = pd.to_datetime(df_user1['Time'])
df_user1_30min = df_user1
df_user1_30min = df_user1.resample('30Min', on='Time').mean().reset_index()
df_user1_30min = df_user1_30min.rename(columns={'Value': 'avg_30_min'})
df_user1_30min = df_user1_30min[['Id', 'Time', 'avg_30_min']]
df_user1_30min = df_user1_30min.dropna()


def calculate_stress_score(avg_30_min):
  if avg_30_min < 65:
    return 0
  elif avg_30_min > 120:
    return 1
  else:
    # Linear interpolation between 65 and 120
    return (avg_30_min - 65) / (120 - 65)

df_user1_30min['stress_score'] = df_user1_30min['avg_30_min'].apply(calculate_stress_score)

print(df_user1_30min.head())
