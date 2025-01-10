import time
import numpy as np
from scipy.signal import find_peaks
from max30102 import MAX30102  
import paho.mqtt.client as mqtt  

# Heart Rate Calculation using IR signal
def calculate_heart_rate(ir_values, sampling_frequency=100):
    if len(ir_values) < sampling_frequency: 
        return 0

    # Find peaks in the IR signal using find_peaks
    peaks, _ = find_peaks(ir_values, distance=sampling_frequency * 0.6) 
    if len(peaks) < 2:
        return 0

    peak_intervals = np.diff(peaks) / sampling_frequency 
    avg_interval = np.mean(peak_intervals)

    bpm = 60 / avg_interval
    return round(bpm)

# Function to calculate SpO2 from Red and IR signals
def calculate_spo2(red_values, ir_values):
    if len(red_values) == 0 or len(ir_values) == 0:
        return 0

    # Calculate the AC and DC components of both Red and IR signals
    red_ac = np.max(red_values) - np.min(red_values)
    ir_ac = np.max(ir_values) - np.min(ir_values)
    red_dc = np.mean(red_values)
    ir_dc = np.mean(ir_values)

    if ir_dc == 0 or red_dc == 0:  
        return 0

    # Ratio of AC/DC for both Red and IR signals
    r_ratio = (red_ac / red_dc) / (ir_ac / ir_dc)

    spo2 = 104 - 17 * r_ratio 
    return max(0, min(100, round(spo2))) 

"""
    Detect sleep stage based on heart rate and SpO2 inputs.
    Calculate sleep mode using heart rate and spo2

    :param heart_rate_value
    :param spo2_value
    :return sleep mode (awake, deep sleep and light sleep) with relevant score
"""

def sleep_mode_detection(heart_rate_value, spo2_value):
    thresholds_values = {
        "LightSleep": {"bpm": (55, 75), "spo2": (92, 97)},
        "DeepSleep": {"bpm": (40, 55), "spo2": (90, 96)},
        "Awake": {"bpm": (75, float('inf')), "spo2": (93, 101)},
    }

    sleep_scores = {}

    for sleep_mode, boundry_values in thresholds_values.items():
        bpm_range = boundry_values["bpm"]
        spo2_range = boundry_values["spo2"]

        bpm_score = 1 if bpm_range[0] <= heart_rate_value <= bpm_range[1] else 0
        spo2_score = 1 if spo2_range[0] <= spo2_value <= spo2_range[1] else 0

        sleep_scores[sleep_mode] = bpm_score + spo2_score

    result_mode = max(sleep_scores, key=sleep_scores.get)
    return result_mode, sleep_scores


# Function to detect when a finger is placed on the sensor
# In here the threshold value is considered as 5000
def is_finger_placed(ir_values):
    threshold = 5000 
    if np.mean(ir_values) > threshold:
        return True
    return False

# MQTT client callbacks
def on_connect(rc):
    print("Connected successfully to MQTT broker" if rc == 0 else f"Failed to connect with result code {rc}")

def on_publish(mid):
    print(f"Message published with ID: {mid}")

# Function to publish the heart rate and SpO2 data via MQTT
def publish_data_via_mqtt(heart_rate, spo2, result_mode):
    broker = "test.mosquitto.org"
    port = 1883
    topic = "sensor/data"

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        client.connect(broker, port)
        client.loop_start()

        message = f"Heart Rate: {heart_rate} BPM, SpO2: {spo2}%, Mode: {result_mode}"
        client.publish(topic, message)
        print(message)

        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"Error: {e}")

# Function to simulate and publish the heart rate and SpO2 data
def simulate_and_publish(red_values, ir_values):
    heart_rate = calculate_heart_rate(ir_values)
    spo2 = calculate_spo2(red_values, ir_values)
    result_mode, score_details = sleep_mode_detection(heart_rate, spo2)

    print(f"Heart Rate: {heart_rate} BPM")
    print(f"SpO2: {spo2}%")
    print(f"Sleep mode: {result_mode}")
    print(f"Score value: {score_details}")

    publish_data_via_mqtt(heart_rate, spo2, result_mode)

# Initialize the MAX30102 sensor
sensor = MAX30102()

red_values = []
ir_values = []

# In here samples per second is consired as 100
sampling_frequency = 100  

# Set a duration for capturing data (35 seconds)
# Capture samples which has 35 seconds data
capture_duration = 5 
capture_samples = capture_duration * sampling_frequency 

# Flag to check if finger is detected
finger_detected = False
print("Finger not detected!")
while True:
    red_values = []
    ir_values = []

    while True:
        # Read raw sensor values IR and Red
        red, ir = sensor.read_fifo()

        # Add the new readings to the signal buffers
        red_values.append(red)
        ir_values.append(ir)

        # Check if a finger is placed on the sensor
        if is_finger_placed(ir_values) and not finger_detected:
            print("Finger detected! Starting to capture data for 35 seconds.")
            finger_detected = True

            # Start collecting data for 35 seconds after detecting the finger
            start_time = time.time()

        # Collect data for exactly 35 seconds after detecting the finger
        if finger_detected:
            # check no of seconds is <= capture duration which is 35
            elapsed_time = time.time() - start_time
            if elapsed_time <= capture_duration:
                pass
            else:
                # After 35 seconds display resuls and calculate heart rate and spo2 values depend on the IR and RED buffer data
                simulate_and_publish(red_values, ir_values)
                print("Data collection complete.")

                # Reset the flag until next finger detection
                finger_detected = False
                print("Finger not detected!")
                break  # Break out of the inner loop to repeat the process

        # Sleep to maintain the sampling rate
        time.sleep(1 / sampling_frequency)

    # Repeat the process indefinitely
    print("Starting the next cycle of data collection...")