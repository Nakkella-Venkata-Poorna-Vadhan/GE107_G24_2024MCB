import serial
import time
import threading
import logging
from flask import Flask
from flask_socketio import SocketIO

# --- 1. CONFIGURATION ---
# CHANGE THIS TO YOUR ARDUINO PORT!
# Windows: 'COM3', 'COM4', etc.
# Mac/Linux: '/dev/ttyUSB0', etc.
SERIAL_PORT = 'COM10' 
BAUD_RATE = 9600

# --- 2. SETUP ---
# Disable Flask logging to keep console clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app, cors_allowed_origins='*')

print("------------------------------------------------")
print(f"Attempting to connect to Arduino on {SERIAL_PORT}...")
print("------------------------------------------------")

# --- 3. SERIAL READING THREAD ---
def read_from_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"✅ SUCCESS: Connected to {SERIAL_PORT}")
        print("   Waiting for LoRa data...")
        
        while True:
            if ser.in_waiting > 0:
                try:
                    # Read line and decode
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    # Check for our "Machine Readable" tag
                    if line.startswith("JSON_DATA:"):
                        # Line format: JSON_DATA:r1:l1:r2:l2:r3:l3
                        parts = line.split(":")
                        
                        if len(parts) >= 7:
                            # Construct the JSON object for the website
                            payload = {
                                "A1": { "rssi": int(parts[1]), "lat": int(parts[2]) },
                                "A2": { "rssi": int(parts[3]), "lat": int(parts[4]) },
                                "A3": { "rssi": int(parts[5]), "lat": int(parts[6]) }
                            }
                            
                            # Send to Website
                            socketio.emit('update', payload)
                            print(f"📡 Data Sent: {payload}")
                            
                except Exception as e:
                    print(f"Error parsing line: {e}")
                    
            time.sleep(0.01) # Tiny sleep to save CPU

    except serial.SerialException:
        print(f"❌ ERROR: Could not open {SERIAL_PORT}.")
        print("   1. Check your USB cable.")
        print("   2. Check if Arduino IDE Serial Monitor is open (CLOSE IT!)")
        print("   3. Update the 'SERIAL_PORT' in server.py")

# Start the Serial Reader in background
thread = threading.Thread(target=read_from_serial)
thread.daemon = True
thread.start()

# --- 4. WEB SERVER ROUTE ---
@app.route('/')
def index():
    with open('./frontend/index.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print("\n🟢 SYSTEM READY!")
    print("   Open your browser and go to: http://localhost:5000")
    print("------------------------------------------------\n")
    socketio.run(app, host='0.0.0.0', port=5000)