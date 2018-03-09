import paho.mqtt.client as mqtt
from planet.Path import Path

CHANNEL = 'explorer/050'
URL = 'robolab.inf.tu-dresden.de'
PORT = 8883


class Communication:
    def __init__(self, planet):
        self.planet = planet
        self.is_connected = False
        self.client = mqtt.Client(client_id='050', clean_session=False, protocol=mqtt.MQTTv31)
        self.client.on_message = self.receive
        self.client.username_pw_set('050', password='gruppe50')

    def receive(self, client, data, message):
        if message:
            topic = message.topic
            payload = message.payload.decode('utf-8').split(' ')
            signature = payload[0]
            command = payload[1]
            if signature is 'ACK':
                if command is 'path' and payload.__len__() == 6:
                    self.receive_edge(payload[2], payload[3], payload[4], payload[5])
                elif command is 'target' and payload.__len__() == 3:
                    self.receive_target(payload[2])
                elif payload.__len__() == 3:
                    self.receive_planet(command, payload[2])
        pass

    def emit(self, payload):
        self.client.publish(CHANNEL, payload, qos=1, retain=False)
        pass

    def start(self):
        if not self.is_connected:
            self.client.connect(URL, port=PORT)
            self.is_connected = True
        self.client.subscribe(CHANNEL, qos=1)
        self.client.loop_start()
        pass

    def stop(self):
        self.client.loop_stop()
        self.is_connected = False
        pass

    # ---------------
    # MESSAGES - OUT
    # ---------------
    def send_exploration_completed(self):
        self.emit('SYN exploration completed!')
        pass

    def send_target_reached(self):
        self.emit('SYN target reached!')
        pass

    def send_ready(self):
        self.emit('SYN ready')
        pass

    def send_edge(self, start: Path, end: Path):
        payload = start.tostring() + ' ' + end.tostring()
        self.emit(payload)

    # ---------------
    # MESSAGES - IN
    # ---------------
    def receive_edge(self, start, end, status, weight):
        start = start.split(',')
        start_direction = start[2]
        start.pop(2)
        end = end.split(',')
        end_direction = end[2]
        end.pop(2)
        pass

    def receive_target(self, target):

        pass

    def receive_planet(self, planet, point):
        CHANNEL = planet
        self.client.subscribe(CHANNEL, qos=1)
        pass
