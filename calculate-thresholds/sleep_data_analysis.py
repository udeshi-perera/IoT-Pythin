import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd

import xml.etree.ElementTree as ET

def read_sleep_records(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    sleep_data = []
    
    # Iterate over all <Record> elements under the root
    for record in root.findall('Record'):
        # Get the attributes for each record
        start_date = record.get('startDate')
        end_date = record.get('endDate')
        value = record.get('value')
        
        # Append the extracted data to the list
        sleep_data.append({
            "startDate": start_date,
            "endDate": end_date,
            "value": value
        })
    
    return sleep_data

# Call the function with the cleaned XML file
sleep_records = read_sleep_records('result_data/Cleaned_Sleep_Analysis.xml')

def parse_sleep_data(sleep_records):
    sleep_data = []
    for record in sleep_records:
        start = datetime.strptime(record['startDate'], "%Y-%m-%d %H:%M:%S %z")
        end = datetime.strptime(record['endDate'], "%Y-%m-%d %H:%M:%S %z")
        sleep_data.append({"start": start, "end": end, "type": record['value']})
    return sleep_data

parsed_sleep_data = parse_sleep_data(sleep_records)

sleep_df = pd.DataFrame(parsed_sleep_data)

print(sleep_df.head(5))

####################################################################################
# Heart beat data

def read_hb_records(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    hb_data = []
    
    # Iterate over all <Record> elements under the root
    for record in root.findall('Record'):
        # Get the attributes for each record
        start_date = record.get('startDate')
        end_date = record.get('endDate')
        value = record.get('value')
        
        # Append the extracted data to the list
        hb_data.append({
            "startDate": start_date,
            "endDate": end_date,
            "value": value
        })
    
    return hb_data

# Call the function with the cleaned XML file
hb_records = read_hb_records('result_data/Cleaned_HB_Analysis.xml')

def parse_hb_data(hb_records):
    hb_data = []
    for record in hb_records:
        start = datetime.strptime(record['startDate'], "%Y-%m-%d %H:%M:%S %z")
        end = datetime.strptime(record['endDate'], "%Y-%m-%d %H:%M:%S %z")
        hb_data.append({"start": start, "end": end, "type": record['value']})
    return hb_data

parsed_hb_data = parse_hb_data(hb_records)

hb_df = pd.DataFrame(parsed_hb_data)

print(hb_df.head(5))


####################################################################################
# spo2 data

def read_spo2_records(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    spo2 = []
    
    # Iterate over all <Record> elements under the root
    for record in root.findall('Record'):
        # Get the attributes for each record
        start_date = record.get('startDate')
        end_date = record.get('endDate')
        value = record.get('value')
        
        # Append the extracted data to the list
        spo2.append({
            "startDate": start_date,
            "endDate": end_date,
            "value": value
        })
    
    return spo2

# Call the function with the cleaned XML file
spo2_records = read_spo2_records('result_data/Cleaned_SPO2_Analysis.xml')


def parse_spo2_data(spo2_records):
    spo2_data = []
    for record in spo2_records:
        start = datetime.strptime(record['startDate'], "%Y-%m-%d %H:%M:%S %z")
        end = datetime.strptime(record['endDate'], "%Y-%m-%d %H:%M:%S %z")
        spo2_data.append({"start": start, "end": end, "type": record['value']})
    return spo2_data

parsed_spo2_data = parse_spo2_data(spo2_records)

spo2_df = pd.DataFrame(parsed_spo2_data)

print(spo2_df.head(5))

def clean_categorical_data(df, column):
    """Cleans a categorical column."""
    df[column] = df[column].astype(str).str.strip()
    return df

def clean_numeric_data(df, column):
    """Cleans a numeric column by extracting valid numbers."""
    df[column] = df[column].astype(str)  # Ensure all values are treated as strings
    df[column] = df[column].str.extract(r'(\d+\.?\d*)')  # Extract valid numbers
    df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert to numeric
    return df.dropna(subset=[column])  # Drop rows with NaN in the column

# Clean each dataset
sleep_df = clean_categorical_data(sleep_df, 'type')  # Sleep data is categorical
heart_df = clean_numeric_data(hb_df, 'type')  # Heartbeat data is numerical
spo2_df = clean_numeric_data(spo2_df, 'type')  # SPO2 data is numerical

import pandas as pd
from datetime import timedelta

def aggregate_data_30min(sleep_df, heart_df, spo2_df):
    # Automatically determine time range from the dataset
    start_time = min(sleep_df['start'].min(), heart_df['start'].min(), spo2_df['start'].min())
    end_time = max(sleep_df['end'].max(), heart_df['start'].max(), spo2_df['start'].max())
    
    interval_minutes = 30
    aggregated = []
    current_start = start_time

    while current_start < end_time:
        current_end = current_start + timedelta(minutes=interval_minutes)
        
        # Heart rate mean
        hb_values = heart_df.loc[
            (heart_df['start'] >= current_start) & (heart_df['start'] < current_end), 'type'
        ]
        hb_mean = hb_values.mean() if not hb_values.empty else None
        
        # SPO2 mean
        spo2_values = spo2_df.loc[
            (spo2_df['start'] >= current_start) & (spo2_df['start'] < current_end), 'type'
        ]
        spo2_mean = spo2_values.mean() if not spo2_values.empty else None
        
        # Dominant sleep type
        sleep_types = sleep_df.loc[
            ((sleep_df['start'] >= current_start) & (sleep_df['start'] < current_end)) |
            ((sleep_df['end'] >= current_start) & (sleep_df['end'] < current_end)), 'type'
        ]
        dominant_sleep_type = sleep_types.mode()[0] if not sleep_types.empty else None

        aggregated.append({
            "interval_start": current_start,
            "interval_end": current_end,
            "mean_heart_rate": hb_mean,
            "mean_spo2": spo2_mean,
            "dominant_sleep_type": dominant_sleep_type
        })
        current_start = current_end

    return pd.DataFrame(aggregated)

aggregated_df = aggregate_data_30min(sleep_df, heart_df, spo2_df)
print(aggregated_df.head(5))

# Convert datetime columns to strings
aggregated_df['interval_start'] = aggregated_df['interval_start'].astype(str)
aggregated_df['interval_end'] = aggregated_df['interval_end'].astype(str)

# Save to Excel
aggregated_df.to_excel('result_data/aggregated_data.xlsx', index=False)

print("Aggregated data has been saved to 'aggregated_data.xlsx'")


