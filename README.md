# DarkEase - Light Control System 
### A Guiding Light for Peaceful and Secure Sleep for Users with Nyctophobia or Similar Preferences

## Project Overview

This is the python application of the project DarkEase that monitors heartbeat and blood oxygen level and control smart lighting to make smooth sleep environment.

### Features:

- MAX30102 Sensor - Measures IR and Red values to calculate heart rate and SpO2 value.
- Sleep Detection Algorithm - By using heart rate and SpO2 value find person's current sleep mode and implemented by score method.
- MQTT Protocol - Communicates with Android application and sends SpO2 value, heart rate and sleep mode.

### Network Configuration:
- Raspberry Pi and Python server must be connected to the same network for optimal performance.
  
## Installation

1. Clone this repository from github: https://github.com/udeshi-perera/IoT-Python.
2. Go to the branch: release/1.0.0
3. Open in Visual Studio Code
4. Install libraries
5. Run sensorvalues.py.
