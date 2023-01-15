import threading
import time
import random
# sensors on car:
# 1. location (longitude, latitude)
# 2. speed 
# 3. direction(left/right -70~70)
# 4. Temperature
# 5. status(stop, running)
# 6. break(true/false)
# 7. proximity
# 8. acceleration


class Sensor:
    def __init__(self, sensor_name) -> None:
        self.sensor_name = sensor_name

class ConditionSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.cond = "Good"
    
    def change_condition(self):
        while True:
            result = random.randint(0, 2)
            if result == 1:
                self.cond = "Bad"
            else:
                self.cond = "Good"
            print("Condition of the road is :{}\n".format(self.cond))
            time.sleep(3)

    def generate_data(self):
        t1 = threading.Thread(target=self.change_condition)
        t1.start()

    def get_condition(self):
        return str(self.cond)

class TrafficLight(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.signal = "green"
    
    def change_signal(self):
        while True:
            result = random.randint(0, 3)
            if result == 0:
                self.signal = "red"
            elif result == 1:
                self.signal = "yellow"
            else:
                self.signal = "green"
            print("Traffic signal ahead is  :{} \n".format(self.signal))
            time.sleep(3)

    def generate_data(self):
        t1 = threading.Thread(target=self.change_signal)
        t1.start()

    def get_signal(self):
        return str(self.signal)

class HumpDistance(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.distance = 100
    
    def generate_data(self):
        t1 = threading.Thread(target=self.change_distance)
        t1.start()

    def change_distance(self):
        while True:
            result = random.randint(0,100)
            self.distance -= result
            if self.distance <=1:
                self.distance = 100
            print("Distance from the hump infront is :{} meters\n".format(self.distance))
            time.sleep(10)

    def get_hump(self):
        return str(self.distance)

class RoadSlope(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.angle = 0

    def change_slope(self):
        while True:
            result = random.randint(-40, 70)
            self.angle = result
            print("Slope of the road now is:{} degree \n".format(self.angle))
            time.sleep(8)
    
    def generate_data(self):
        t1 = threading.Thread(target=self.change_slope)
        t1.start()
    
    def get_slope(self):
        return str(self.angle)

class CongestionDistance(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.number_of_vehicles = 10
    
    def increase_congestion(self):
        while True:
            time.sleep(3)
            vehicles = random.randint(0,100)
            self.number_of_vehicles += vehicles
            if self.number_of_vehicles > 70:
                self.number_of_vehicles = 10
            print("Traffic congestion ahead with number of vehciles = {}\n".format(self.number_of_vehicles))
            time.sleep(3)

    def generate_data(self):
        t1 = threading.Thread(target=self.increase_congestion)
        t1.start()
        time.sleep(1)

    def get_congestion(self):
        return str(self.number_of_vehicles)


class NextUTurn(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.distance = 2000
    
    def decrease_distance(self):
        while True:
            time.sleep(3)
            dist = random.randint(0,1999)
            self.distance -= dist
            if self.distance <50:
                self.distance = 2000
            print("Next U turn in : {} meters \n".format(self.distance))
    
    def generate_data(self):
        t1 = threading.Thread(target=self.decrease_distance)
        t1.start()
        time.sleep(1)
    
    def get_uturn_distance(self):
        return str(self.distance)







