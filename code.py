import requests
import RPi.GPIO as GPIO
import time
from datetime import datetime
from pytimedinput import timedInput

try:
    # Set the GPIO mode to BCM
    GPIO.setmode(GPIO.BCM)

    # Define the GPIO pin used to control the relay
    relay_pin = 17

    # Set the GPIO pin as an output
    GPIO.setup(relay_pin, GPIO.OUT)
    print("Frost Heave Apparatus Setup")
    print("===========================")
    time.sleep(1)
    
    oft = int(input("Enter how often you want to take a measurment in minutes: "))
    oftSec = oft*60
    time.sleep(1)
    print("Okay, I will wait "+str(oft)+" minutes to take each measurment.")
    time.sleep(1)
    duration = int(input("Enter how many hours you want this program to run for: "))
    time.sleep(1)
    print("Okay, I will run the program and take measurments for "+str(duration)+" hours")
    time.sleep(1)
    durationMinutes = int(duration)*60
    loopTimes = durationMinutes/oft
    print("That means I will take a measurment a total of "+str(loopTimes)+" times")
    time.sleep(1)
    print("===================")
    print("IMPORTANT:")
    print("1. If you want to cancel this earlier, then hit ctr + c to cancel")
    time.sleep(1)
    print("2. Do not click outside the terminal while program is running! (if you do click back in it)") 
    print("===================")
    time.sleep(1)
    print("Taking the first measurment....")
    
    i = 1
    while i <= loopTimes:
        i = i + 1
        try:
            
            
            # Turn on the relay
            GPIO.output(relay_pin, GPIO.HIGH)
            #value = input("Automaticly measured value:\n")
            value, timedOut = timedInput("Please, do enter something: ")

            print("Relay turned on")

            # Wait for 1 second
            time.sleep(.18)

            # Turn off the relay
            GPIO.output(relay_pin, GPIO.LOW)
            
            print("Relay turned off")

            print(f'Value measured: {value}')

            file = open("/media/pi/UDISK/FrostHeave/log.csv","a")
            file.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S')+","+value+"\n")
            file.close()
            print("Saved to thumdrive")
            
            time.sleep(oftSec)

        except KeyboardInterrupt:
            # Cleanup on keyboard interrupt
            GPIO.cleanup()
            break  # Exit the loop on KeyboardInterrupt

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Cleanup GPIO on normal program exit
    GPIO.cleanup()
