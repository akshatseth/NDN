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

class SpeedSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        if sensor_name == 'bike':
            self.speed = 10
        else:
            self.speed = 50
    
    def change_speed(self):
        while True:
            result = random.randint(0, 2)
            if self.sensor_name == 'bike':
                if result == 1 and self.speed <= 18:
                    self.speed += 2
                elif self.speed >= 15:
                    self.speed -= 2
            else:
                if result == 1 and self.speed <= 60:
                    self.speed += 25
                elif self.speed >= 55:
                    self.speed -= 18
            print("Speed of truck  is :{} km/h\n".format(self.speed))
            time.sleep(3)

    def generate_data(self):
        t1 = threading.Thread(target=self.change_speed)
        t1.start()

    def get_speed(self):
        return str(self.speed)

class ProximitySensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.proximity = 20
    
    def change_proximity(self):
        while True:
            result = random.randint(0, 2)
            if result == 1 and self.proximity <= 9:
                self.proximity += 3
            elif self.proximity >= 10:
                self.proximity -= 2
            print("Proximity between the vehicles:{} metres\n".format(self.proximity))
            time.sleep(3)

    def generate_data(self):
        t1 = threading.Thread(target=self.change_proximity)
        t1.start()

    def get_proximity(self):
        return str(self.proximity)

class LocationSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.latitude = 53.34687
        self.longitude = -6.25948
    
    def generate_data(self):
        t1 = threading.Thread(target=self.change_gps)
        t1.start()

    def change_gps(self):
        while True:
            self.latitude += 0.002
            self.longitude += 0.001
            print("Position of the vehicle is:{} latitude and {} longitude\n".format(self.latitude, self.longitude))
            time.sleep(10)


    def get_location(self):
        return '%f,%f' % (self.latitude, self.longitude)

class DirectionSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.angle = 0

    def generate_data(self):
        result = random.randint(-70, 70)
        self.angle = result
        print("Direction in which vehicle is heading\n:{}".format(self.angle))
        time.sleep(8)

    def get_direction(self):
        return str(self.angle)

class TemperatureSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.temperature = 75
    
    def change_temp(self):
        while True:
            time.sleep(3)
            result = random.randint(0, 2)
            if result == 1:
                self.temperature += random.randint(0,40)
            else:
                self.temperature -= random.randint(0,15)
            print("Temperature of Truck engine is :{} degree celcius\n".format(self.temperature))

    def generate_data(self):
        t1 = threading.Thread(target=self.change_temp)
        t1.start()
        time.sleep(1)

    def get_temperature(self):
        return str(self.temperature)

class PressureSensor(Sensor):
    def __init__(self, sensor_name)->None:
        super().__init__(sensor_name)
        self.pressure = 40

    
    def change_pressure(self):
        while True:
            time.sleep(3)
            result = random.randint(0, 18)
            self.pressure = self.pressure - result
            if self.pressure <10:
                self.pressure = 40
            print("Current tyre pressure is {} psi\n".format(self.pressure))

    def generate_data(self):
        t1 = threading.Thread(target=self.change_pressure)
        t1.start()
        time.sleep(2)

    def get_pressure(self):
        return str(self.pressure)

# status(stop, running)
class StatusSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.status = 'run'
    
    def change_status(self): 
        result = random.randint(0, 3)
        if result == 1:
            self.status = 'stop'
        else:
            self.status = 'running'
        print("Status of the vehicle is {}\n".format(self.status))

    def get_status(self):
        self.change_status()
        return self.status


class weightLoad(Sensor):
    def __init__(self, sensor_name)->None:
        super().__init__(sensor_name)
        self.load = 100

    def change_load(self):
        while True:
            time.sleep(3)
            new_load = random.randint(0,100)
            self.load+= new_load
            if self.load >600:
                self.load = 100
            print("Load in the truck is total of {} tons\n".format(self.load))
            time.sleep(7)
    

    def generate_data(self):
        t1 = threading.Thread(target=self.change_load)
        t1.start()

    def get_load(self):
        return str(self.load)


# m/s^2
class SpeedupSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.speedup = 0

    def get_speedup(self):
        if (self.sensor_name == 'bike'):
            self.proxity = random.randint(0, 0.6)
        else:
            self.proxity = random.randint(0, 2)
        return str(self.proxity)

