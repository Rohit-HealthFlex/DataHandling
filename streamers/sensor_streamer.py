import serial

x = 'FA:21:224:A3:8A:02'
with serial.Serial('COM5', 19200, timeout=1) as ser:
    s = ser.read(10)        # read up to ten bytes (timeout)
    line = ser.readline()   # read a '\n' terminated line
