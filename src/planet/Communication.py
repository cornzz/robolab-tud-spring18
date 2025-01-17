import paho.mqtt.client as mqtt
from .Direction import Direction
from .Vertex import Vertex
from .Path import Path
from .Edge import Edge


URL = 'robolab.inf.tu-dresden.de'
PORT = 8883


class Communication:
    def __init__(self, planet, odometry):
        self.CHANNEL = 'explorer/050'
        self.planet = planet
        self.is_connected = False
        self.client = mqtt.Client(client_id='050', clean_session=False, protocol=mqtt.MQTTv31)
        self.client.on_message = self.receive
        self.client.username_pw_set('050', password='Cbqs7BF5LS')
        self.edge_send = None
        self.test_planet = 'Vulcan'
        self.odometry = odometry

    def receive(self, client, data, message):
        if message:
            topic = message.topic
            payload = message.payload.decode('utf-8').split(' ')
            signature = payload[0]
            command = payload[1]
            print('Message received: ', message.payload.decode('utf-8'))
            if signature == 'ACK':
                if command == 'path' and payload.__len__() == 6:
                    self.receive_edge(payload[2], payload[3], payload[4], payload[5])
                elif command == 'target' and payload.__len__() == 3:
                    self.receive_target(payload[2])
                elif payload.__len__() == 3:
                    self.receive_planet(command, payload[2])
        pass

    def emit(self, payload):
        payload = 'SYN ' + payload
        print('Message send: ', payload)
        self.client.publish(self.CHANNEL, payload, qos=1, retain=False)
        pass

    def start(self):
        if not self.is_connected:
            self.client.connect(URL, port=PORT)
            self.is_connected = True
        self.client.subscribe(self.CHANNEL, qos=1)
        self.client.loop_start()
        pass

    def stop(self):
        self.client.loop_stop()
        self.is_connected = False
        pass

    # ---------------
    # MESSAGES - OUT
    # ---------------
    def hallo_kilian(self):
        self.emit('HALLO KILIAN! :D')
        pass

    def send_test_planet(self):
        self.emit('testplanet ' + self.test_planet)
        pass

    def send_exploration_completed(self):
        self.emit('exploration completed!')
        pass

    def send_target_reached(self):
        self.emit('target reached!')
        pass

    def send_ready(self):
        self.emit('ready')
        pass

    def send_edge(self, edge: Edge, status):
        start_x = str(edge.start.position[0])
        start_y = str(edge.start.position[1])
        start_direction = Direction.str(edge.start_direction, False)
        end_x = str(edge.end.position[0])
        end_y = str(edge.end.position[1])
        end_direction = Direction.str(edge.end_direction, False)
        start_str = start_x + ',' + start_y + ',' + start_direction
        end_str = end_x + ',' + end_y + ',' + end_direction
        payload = 'path ' + start_str + ' ' + end_str + ' ' + status
        self.edge_send = edge
        self.emit(payload)

    # ---------------
    # MESSAGES - IN
    # ---------------
    def receive_edge(self, start, end, status, weight):
        start = start.split(',')
        end = end.split(',')

        start_x = int(start[0])
        start_y = int(start[1])
        start_direction = Direction.num(start[2])
        end_x = int(end[0])
        end_y = int(end[1])
        end_direction = Direction.num(end[2])

        start_vertex = Vertex((start_x, start_y))
        end_vertex = Vertex((end_x, end_y))
        edge = Edge(start_vertex, end_vertex, start_direction, end_direction, float(weight))
        print('edges: ', edge, self.edge_send)
        if self.edge_send is not None and edge is not None and edge.start.position == self.edge_send.start.position:
            self.planet.vertexes[edge.end.id] = edge.end
            self.planet.set_curr_vertex(edge.end)
            self.odometry.set_position(edge.end.position)
            self.planet.edges[edge.id] = edge
            print('edge changes applied: ', self.planet.edges[edge.id])
            if self.edge_send in self.planet.edges:
                del self.planet.edges[self.edge_send.id]
                print('edge deleted: ', self.edge_send.id)
            if self.edge_send.end in self.planet.vertexes:
                del self.planet.vertexes[self.edge_send.end.id]
                print('vertex deleted: ', self.edge_send.end.id)
            for path in self.planet.paths.values():
                if self.edge_send.start == path.source.position:
                    self.planet.paths[path.id] = Path(edge.start, path.direction)
        else:
            path_to = Path(edge.start, edge.start_direction)
            path_from = Path(edge.end, edge.end_direction)
            self.planet.vertexes[edge.start.id] = edge.start
            self.planet.vertexes[edge.end.id] = edge.end
            self.planet.add_edge(path_to, path_from, float(weight), True)
        self.edge_send = None
        pass

    def receive_target(self, target):
        target = target.split(',')
        target_pos = (int(target[0]), int(target[1]))
        print('received target: ', target, target_pos)
        vertex = self.planet.vertex_exists(target_pos)
        if vertex:
            print('Target known!')
            self.planet.get_shortest_path(vertex)
            self.planet.set_target_mode()
        else:
            print('Target unknown!')
            vertex = self.planet.add_vertex(target_pos)
        self.planet.set_target(vertex)
        pass

    def receive_planet(self, planet, point):
        self.CHANNEL = 'planet/' + planet
        self.client.subscribe(self.CHANNEL, qos=1)
        point = point.split(',')
        vertex = Vertex((point[0], point[1]))
        self.planet.set_curr_vertex(vertex)
        pass
