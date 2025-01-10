import pandas as pd
import numpy as np

# Load the filtered data from excell
df = pd.read_excel('result_data/filtered_aggregated_data.xlsx')

# Group the data by the 'dominant_sleep_type' to analyze the heart rate and SPO2 for each sleep mode
grouped = df.groupby('dominant_sleep_type')

# Prepare a dictionary to store threshold values reference to the sleep mode
thresholds = {}

def calculate_sleepmode_thresholds(group):
    # Calculate the mean, standard deviation, and percentiles for heart rate and SPO2
    mean_heart_rate = group['mean_heart_rate']
    mean_spo2 = group['mean_spo2']
    
    # Heart rate thresholds using IQR and percentiles
    heart_rate_iqr = np.percentile(mean_heart_rate, 75) - np.percentile(mean_heart_rate, 25)
    heart_rate_lower = np.percentile(mean_heart_rate, 25) - 1.5 * heart_rate_iqr
    heart_rate_upper = np.percentile(mean_heart_rate, 75) + 1.5 * heart_rate_iqr
    heart_rate_mean = mean_heart_rate.mean()
    heart_rate_std = mean_heart_rate.std()
    
    # SPO2 thresholds using IQR and percentiles
    spo2_iqr = np.percentile(mean_spo2, 75) - np.percentile(mean_spo2, 25)
    spo2_lower = np.percentile(mean_spo2, 25) - 1.5 * spo2_iqr
    spo2_upper = np.percentile(mean_spo2, 75) + 1.5 * spo2_iqr
    spo2_mean = mean_spo2.mean()
    spo2_std = mean_spo2.std()
    
    # Return the threshold dictionary
    return {
        'heart_rate_mean': heart_rate_mean,
        'heart_rate_std': heart_rate_std,
        'heart_rate_lower_threshold': heart_rate_lower,
        'heart_rate_upper_threshold': heart_rate_upper,
        'spo2_mean': spo2_mean,
        'spo2_std': spo2_std,
        'spo2_lower_threshold': spo2_lower,
        'spo2_upper_threshold': spo2_upper
    }

# Iterate over the grouped data and calculate thresholds
for sleep_mode, group in grouped:
    thresholds[sleep_mode] = calculate_sleepmode_thresholds(group)

# Convert the dictionary to a DataFrame 
threshold_df = pd.DataFrame.from_dict(thresholds, orient='index')

# Save the threshold data to sleep_mode_thresholds excel file
threshold_df.to_excel('result_data/sleep_mode_thresholds.xlsx')

print("Threshold values for each sleep mode have been saved to 'sleep_mode_thresholds.xlsx'")
