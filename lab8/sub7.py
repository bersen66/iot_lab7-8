import copy
import paho.mqtt.client as mqtt
import datetime
import json
import dict2xml
import asyncio
import aiofiles


mqtt_broker = "test.mosquitto.org"


class Results:
    '''Stores values of devices'''

    def __init__(self, topics_num=0):
        self.topics_num = topics_num
        self.current_entry = {}
        self.backbone = []

    def add_topic(self, topicname):
        self.current_entry[topicname] = None

    def get_current_entry(self) -> dict:
        return self.current_entry

    def flush(self):

        if self.__not_all_topics_recived__():
            return


        self.current_entry["time"] = str(datetime.datetime.now().time().strftime("%H:%M:%S"))
        self.backbone.append(copy.copy(self.current_entry))
        print(self.backbone)
        self.current_entry.clear()

    def __not_all_topics_recived__(self):
        return len(self.current_entry) < self.topics_num

    def __str__(self) -> str:
        return str(self.backbone)

    def to_json(self) -> str:
        return json.dumps(self.backbone)

    def to_xml(self) -> str:
        res = {"result" : self.backbone}   
        return dict2xml.dict2xml(res, wrap='root')

async def save_in_json(data: Results, filepath: str = "res.json"):
    async with aiofiles.open(filepath, mode='w') as f:
        await f.write(data.to_json())

async def save_in_xml(data: Results, filepath="res.xml"):
    async with aiofiles.open(filepath, mode='w') as f:
        await f.write(data.to_xml())


TOPICS = [
    "/devices/wb-msw-v3_21/controls/CO2",
    "/devices/wb-msw-v3_21/controls/Sound Level",
    "/devices/wb-ms_11/controls/Illuminance",
    "/devices/wb-msw-v3_21/controls/Temperature"
]

history = Results(topics_num=len(TOPICS))


def on_message(client, userdata, msg):
    print(f"{msg.topic} msg: msg value: {msg.payload.decode()}")
    current_entry = history.get_current_entry()
    topic = str(msg.topic.split('/')[-1])
    current_entry[topic] = int(msg.payload.decode())

    if (current_entry[topic] is not None):
        history.flush()


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code: {rc}')
    subscribe_to_topics(client=client)


def subscribe_to_topics(client):
    for topic in TOPICS:
        client.subscribe(topic)


async def main():
    client = mqtt.Client()

    # seting up callbacks for basic events
    client.on_connect = on_connect

    client.connect(mqtt_broker, port=1883, keepalive=60)
    client._on_message = on_message
    client.loop_start()  # callbacks are running in other thread

    while True:
        await asyncio.sleep(5)
        history.flush()
        await save_in_json(history)
        await save_in_xml(history)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bye!")
