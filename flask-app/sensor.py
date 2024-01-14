import serial
import time


def emit_sensor_data(socketio):
    last_val = 0
    arduino = None

    serial_port = '/dev/cu.usbmodem1101'
    try:
        arduino = serial.Serial(serial_port, 9600, timeout=1)
        time.sleep(2)
        arduino.flushInput()

        print("Serial connection established on", serial_port)
        while True:
            # print("Listening...")
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').rstrip()
                socketio.emit('sensor', {'data': line})
                print(">>>> ", line, end="\r                \r")    
                time.sleep(0.4)
                
    except KeyboardInterrupt:
        print("Program terminated by user")
    except serial.SerialException:
        print(f"Could not open serial port {serial_port}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        arduino.close()
        print("Serial port closed")
    