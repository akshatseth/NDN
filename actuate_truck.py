import socket
import time
import base64
import random
from cryptography.fernet import Fernet

encrypt_decrypt_key = b'GyrNsdgaGZo7PC7xMTjG_h9Wgv9vkD7jXsORLbKeeWo='
fernet = Fernet(encrypt_decrypt_key)

ROUTER_IP = '10.35.70.24'
ROUTER_PORT = 33359

BACKUP_ROUTER_IP = '10.35.70.45'
BACKUP_ROUTER_PORT = 33359

truck1_proximity = 0
truck1_speed = 50
truck1_direction = 'forward'
truck1_status = 'running'
truck2_speed = 0

def bencode(toEncode):
    ascii_encoded = toEncode.encode("ascii")
    base64_bytes = base64.b64encode(ascii_encoded)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def bdecode(toDecode):
    base64_bytes = toDecode.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string

# use case 1, truck should be in the range of speed in the front


def regulate_speed(speed1, speed2):
    speed_diff = abs(speed1 - speed2)
    if(speed_diff)>5:
        print("Difference in speed is increasing, accelearting to increase speed")

def take_a_decision(speed,proximity, direction, status):
    if speed>40 and proximity < 10:
        print("Applying brakes to avoid collision")
    if direction != 0:
        print("Changing direction of the vehicle to follow the truck infront :{} degree turn".format(direction))
    if status == 'stop':
        print("Stopping the truck")


def actuate(interest_packet, data_packet):
    print("\033[92m"+"Data packet receieved \033[92m", data_packet)
    if interest_packet == 'truck1/proximity':
        global truck1_proximity
        truck1_proximity = float(data_packet)
        print("Distance from the truck infront is:{} metres".format(data_packet))
    if interest_packet == 'truck1/speed':
        global truck1_speed
        truck1_speed = float(data_packet)
        print("Truck infront is going at speed:{} km/h".format(data_packet))
    if interest_packet == 'truck1/direction':
        global truck1_direction
        truck1_direction = data_packet
        print("Truck infront is taking a turn towards :{}".format(data_packet))
    if interest_packet == 'truck1/status':
        global truck1_status
        truck1_status = data_packet
        print("Running status of truck infront is:{}".format(data_packet))
    if interest_packet == 'truck2/speed':
        global truck2_speed
        truck2_speed = float(data_packet)
        print("Speed of truck2 is {} km/h".format(truck2_speed))
    if interest_packet == 'road/condition':
        if data_packet == 'Good':
            print("Road ahead is good, safe to increase speed")
        else:
            print("Road ahead is not in a good condition, be cautious")
    if interest_packet == 'road/trafficlight':
        if data_packet == 'red':
            print("Alert, stop the vehicle")
        elif data_packet =='yellow':
            print("Look and go")
        else:
            print("Keep going")
    if interest_packet == 'road/hump':
        dist = float(data_packet)
        if dist<30:
            print("Slow down, speed breaker ahead")
        else:
            print("Speedbreaker at a distane of:{}".format(dist))
    if interest_packet == 'road/slope':
        slope = float(data_packet)
        if slope>25:
            print("Lowering the gear in the car because of the inclination")
        if slope <0:
            print("Swithing off engine to save fuel due to downwards slope")
    if interest_packet == 'road/congestion':
        congestion = float(data_packet)
        if congestion >40:
            print("Traffic congestion ahead, take an alternative route")
        else:
            print("Traffic clear ahead")
    if interest_packet == 'road/uturn':
        dist = float(data_packet)
        if dist < 500:
            print("U turn coming in {} meters".format(dist))
        else:
            print("No U turn for next 2 kms")
    if interest_packet == 'car/temperature':
        temp = float(data_packet)
        if temp>100:
            print("Car engine is overheating, releasing the coolant")
        else:
            print("Car engine is at temperature :{} degree celcius".format(temp))
    if interest_packet == 'car/pressure':
        pressure = float(data_packet)
        if pressure < 30:
            print("Car tyre pressure is less than standard, please fill air")
        else:
            print("Current car tyre pressure is:{} psi".format(data_packet))
    if interest_packet == 'car/petrol':
        petrol = float(data_packet)
        if petrol < 3:
            print("Petrol quantity is less, please fill at nearest station")
        else:
            print("Current petrol in the car is :{} litres".format(petrol))
    if interest_packet == 'car/aircondition':
        ac = float(data_packet)
        if ac < 15:
            print("Car is too cold, swithcing off AC")
        else:
            print("Current AC temperature inside car :{} degree celcius".format(ac))
    if interest_packet == 'bike/gear':
        gear = float(data_packet)
        print("Curren gear the bike is running in is {}".format(gear))
    if interest_packet == 'bike/petrol':
        petrol = float(data_packet)
        if petrol < 3:
            print("Petrol quantity is less, please fill at nearest station")
        else:
            print("Current petrol in the car is :{} litres".format(petrol))
    if interest_packet == 'bike/proximity':
        prox = float(data_packet)
        if prox < 10:
            print("Too close to a nearby vehicle, be cautious!!!")
    if interest_packet == 'tractor/speed':
        print("Current speed of tractor is :{}".format(data_packet))
    if interest_packet == 'superbike/gear':
        print("Current gear for the superbike is :{}".format(data_packet))
    


def sendInterest(interest):
        print('\n\033[94m' + 'attempting to send interest packet:{}\n \033[94m'.format(interest))
           
        try:
            router = (ROUTER_IP, ROUTER_PORT)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(router)
            base64encoded = str(bencode(interest))
            s.send(fernet.encrypt(base64encoded.encode()))
            ack = s.recv(1024)
            print("Acknowledgement received in origin", ack)
            data_packet = fernet.decrypt(ack)
            data_packet = bdecode(data_packet.decode())
            print("What is data packet", data_packet)

            if data_packet != "404 not found":
                actuate(interest, data_packet)
            else:
                print("404 Interest Packet not found\n")
            s.close()
        except:
            print("Primary Router Unavailable, switching to secondary")
            backup_router = (BACKUP_ROUTER_IP, BACKUP_ROUTER_PORT)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(backup_router)
            base64encoded = str(bencode(interest))
            s.send(fernet.encrypt(base64encoded.encode()))
            ack = s.recv(1024)
            print("Acknowledgement received in origin", ack)

            data_packet = fernet.decrypt(ack)
            data_packet = bdecode(data_packet.decode())
            print("What is data packet", data_packet)
            if data_packet != "404 not found":
                actuate(interest, data_packet)
            else:
                print("404 Interest Packet not found\n")
            s.close()


def main():
    interest_truck = ["truck1/proximity","truck1/speed","truck1/direction","truck1/status","truck2/speed"]
    interest_road = ["road/condition","road/trafficlight","road/hump","road/slope","road/congestion","road/uturn"]
    interest_car_and_bike = ["car/temperature","car/pressure","car/petrol","car/aircondition","bike/gear","bike/petrol","bike/proximity"]
    interest_other_group = ["tractor/speed","superbike/gear"]

    while True:
        print('\n')
        print('1. For truck use case')
        print('2. For road use case')
        print('3. For car and bike use case')
        print('4. Send interest to other groups')
        choice = input()
        if choice == '1':
            for i in interest_truck:
                sendInterest(i)
            regulate_speed(truck1_speed, truck2_speed)
            print("\n")
            take_a_decision(truck1_speed, truck1_proximity,  truck1_direction, truck1_status)
            print("\n")
        if choice == '2':
            for i in interest_road:
                sendInterest(i)
        if choice == '3':
            for i in interest_car_and_bike:
                sendInterest(i)
        if choice == '4':
            for i in interest_other_group:
                sendInterest(i)
        



if __name__ == '__main__':
    main()
