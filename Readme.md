# Project Setup Guide (Local Access)

This README explains how **anyone** can run the project locally on their own computer without hosting it online.

---

## ✅ 1. Requirements

Make sure the user has:

- **Python 3.8+**
- Required Python libraries:
  - `flask`
  - `flask_socketio`
  - `pyserial`

Install them using:

```
pip install flask flask_socketio pyserial
```

---

## ✅ 2. Folder Structure

The project should be arranged like this:

```
project/
│── backend/
│     ├── server.py
│
└── frontend/
      ├── index.html
      └── assets/
```

---

## ✅ 3. Update Serial Port

Before running, the user **must edit `server.py`**:

```python
SERIAL_PORT = 'COM10'
```

Change `'COM10'` to the correct port used on their computer.

### ✔ Common Example Ports:
- Windows: `COM3`, `COM4`, `COM5`, etc.
- Linux: `/dev/ttyUSB0`, `/dev/ttyACM0`
- Mac: `/dev/cu.usbmodem####`

---

## ✅ 4. Connect the LoRa Receiver

1. Plug the LoRa/Arduino receiver into the computer via USB  
2. Check the COM port in Device Manager or `/dev`  
3. Update the `SERIAL_PORT` in `server.py`  
4. **Close Arduino IDE Serial Monitor**

---

## ✅ 5. Run the Backend

Open a terminal inside the backend folder:

```
cd backend
python server.py
```

Expected output:

```
SYSTEM READY!
Connected to COMX
Waiting for LoRa data...
```

---

## ✅ 6. Access the Frontend

Open the site in any browser:

```
http://localhost:5000
```

---

## 🔄 7. For Any New User

1. Install Python  
2. Install libraries  
3. Connect LoRa receiver  
4. Update `SERIAL_PORT`  
5. Run backend  
6. Visit `localhost:5000`  

---

## ❗ Notes

- Only **one program** can use the serial port  
- Keep the backend terminal open  
- Data will appear automatically when packets arrive  

---

## 🎉 Done!

Your project now works **on any computer** following this guide.
