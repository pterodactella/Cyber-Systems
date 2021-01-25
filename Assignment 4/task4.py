import requests
import sys
import time
import datetime
import json

time_now = datetime.datetime.now

def main():
    r = requests.get('http://192.168.4.1/sensor/temp')
    return r.json()

def log_data(path):
    with open(path, "w") as f:
        try:
            while True:
                f.write("{} {}\n".format(time_now(),main()))
                print("{} {} Celsius\n".format(time_now(),main()))
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted, quitting the program...")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Too few arguments. Please input python task4.py <path for the file>")
        exit()
    path = sys.argv[1]
    log_data(path)
        