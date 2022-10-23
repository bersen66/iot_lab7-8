import random
import time
import paho.mqtt.publish as publish

topics = [
    "/devices/wb-msw-v3_21/controls/CO2",
    "/devices/wb-msw-v3_21/controls/Sound Level",
    "/devices/wb-ms_11/controls/Illuminance",
    "/devices/wb-msw-v3_21/controls/Temperature"
]

hostname = 'test.mosquitto.org'



def main():
    while True:
        for topic in topics:
            publish.single(topic, str(random.randint(1, 100)), hostname=hostname)
        time.sleep(2)



if __name__ == '__main__':
    main()
