import serial

try:
    ser = serial.Serial('/dev/ttyAMA10', 115200, timeout=1)
    print("Serial connection established!")
    ser.close()
except Exception as e:
    print("Error:", str(e))
