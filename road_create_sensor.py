# sensors on car:
# 1. location (longitude, latitude)
# 2. speed 
# 3. direction(left/right -70~70)
# 4. temperature
# 5. status(stop, running)
# 6. heading (0-360)
# 7. acceleration
# 8. proximity

import socket
import time
import traceback
import random
import base64
from road_sensor import *
import threading
from cryptography.fernet import Fernet


encrypt_decrypt_key = b'GyrNsdgaGZo7PC7xMTjG_h9Wgv9vkD7jXsORLbKeeWo='
fernet = Fernet(encrypt_decrypt_key)


class Vehicle:
    def __init__(self, vehicle_type, router_host, router_port,backup_router_host,backup_router_port,port):
        self.router_host = router_host
        self.router_port = router_port
        self.backup_router_host = backup_router_host
        self.backup_router_port = backup_router_port

        hostname = socket.gethostname()
        self.host = socket.gethostbyname(hostname)
        self.port = port
        print('self.host ' + self.host + ' port: ' + str(self.port))
        self.vehicle_type = vehicle_type

        self.condition_sensor = ConditionSensor('%s/condition' % self.vehicle_type)
        self.traffic_light_sensor = TrafficLight('%s/trafficlight' % self.vehicle_type)
        self.hump_sensor = HumpDistance('%s/hump' % self.vehicle_type)
        self.slope_sensor = RoadSlope('%s/slope' % self.vehicle_type)
        self.congestion_sensor = CongestionDistance('%s/congestion' % self.vehicle_type)
        self.uturn_sensor = NextUTurn('%s/uturn' % self.vehicle_type)
        self.advertise_string = '[%s/condition, %s/trafficlight, %s/hump, %s/slope, \
            %s/congestion, %s/uturn]' % (self.vehicle_type, self.vehicle_type, self.vehicle_type, self.vehicle_type,
            self.vehicle_type, self.vehicle_type)

    def advertiseFeature(self):
        """Advertise the host IP."""
        while True:
            print("ADVERTISING")

            try:
                server_tup = (self.router_host, self.router_port)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(server_tup)
                message = f'HOST {self.host} PORT {self.port} ACTION {self.advertise_string}'
                print('Advertising ', message)
                s.send(message.encode())
                s.close()
            except:
                backup_tup = (self.backup_router_host, self.backup_router_port)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(backup_tup)
                message = f'HOST {self.host} PORT {self.port} ACTION {self.advertise_string}'
                print('Advertising ', message)
                s.send(message.encode())
                s.close()

    def create_sensors(self):
        self.condition_sensor.generate_data()
        self.traffic_light_sensor.generate_data()
        self.hump_sensor.generate_data()
        self.slope_sensor.generate_data()
        self.congestion_sensor.generate_data()
        self.uturn_sensor.generate_data()

    
    def bencode(self, toEncode):
        ascii_encoded = toEncode.encode("ascii")
        base64_bytes = base64.b64encode(ascii_encoded)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def bdecode(self, toDecode):
        base64_bytes = toDecode.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string

    def sendAck(self, conn, raddr, result):
        """Send sensor data to all peers."""
        try:
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.connect((raddr, SENSOR_PORT))
            msg = result
            conn.send(fernet.encrypt(self.bencode(msg).encode()))
            # sent = True
            # s.close()
        except Exception:
            print(traceback.format_exc())
            print('exception occurred while sending acknowledgement: ', Exception)


# self.advertise_string = '[%s/location, %s/speed, %s/direction, %s/temperature, \
#             %s/status, %s/heading, %s/speedup, %s/proximity]'

    def callActuator(self, interest):
        if interest.lower() == "condition":
            return self.condition_sensor.get_condition()
        elif interest.lower() == "trafficlight":
            return self.traffic_light_sensor.get_signal()
        elif interest.lower() == "hump":
            return self.hump_sensor.get_hump()
        elif interest.lower() == "slope":
            return self.slope_sensor.get_slope()
        elif interest.lower() == 'congestion':
            return self.congestion_sensor.get_congestion()
        elif interest.lower() == "uturn":
            return self.uturn_sensor.get_uturn_distance()

    def receiveData(self):
            print("listening for actuation requests")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hostname = socket.gethostname()
            host = socket.gethostbyname(hostname)
            print('self.host ' + self.host)
            s.bind((host, self.port))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                print("addr: ", addr[0])
                # print("connection: ", str(conn))
                data = conn.recv(1024)
                data = fernet.decrypt(data)
                data = self.bdecode(data.decode())

                print(data, " to actuate on")
                # call actuators
                [vehicle_type, interest] = data.split('/')
                print("get interest %s " % vehicle_type)
                if self.vehicle_type == vehicle_type:
                    actuationResult = self.callActuator(interest)
                    self.sendAck(conn, addr[0], actuationResult)
                    conn.close()
                time.sleep(1)

def main():

    peer_port = 33341    # Port for listening to other peers

    router_host = '10.35.70.24'
    router_port = 33334

    backup_router_host = '10.35.70.45'
    backup_router_port = 33334

    road = Vehicle('road', router_host, router_port,backup_router_host,backup_router_port, peer_port)
    t1 = threading.Thread(target=road.advertiseFeature)
    t1.start()

    road.create_sensors()

    while True:
        road.receiveData()

if __name__ == '__main__':
    main()