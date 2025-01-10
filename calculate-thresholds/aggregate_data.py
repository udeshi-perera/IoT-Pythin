import pandas as pd

# Load the data from the aggregated data excel file
df = pd.read_excel('result_data/aggregated_data.xlsx')

# Filter rnon-missing value rows in 'mean_heart_rate', 'mean_spo2', and 'dominant_sleep_type'
filtered_df = df.dropna(subset=['mean_heart_rate', 'mean_spo2', 'dominant_sleep_type'])

# Save the filtered rows to excel file
filtered_df.to_excel('result_data/filtered_aggregated_data.xlsx', index=False)

print("Filtered data has been saved to 'filtered_aggregated_data.xlsx'")
