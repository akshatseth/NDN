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
        self.speed = 60
    
    def change_speed(self):
        while True:
            time.sleep(3)
            result = random.randint(0, 2)
            if result == 1 and self.speed <= 60:
                self.speed += 25
            elif self.speed >= 55:
                self.speed -= 18
            print("Speed of car is :{} km/h\n".format(self.speed))


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
            time.sleep(3)
            result = random.randint(0, 2)
            if result == 1 and self.proximity <= 9:
                self.proximity += 3
            elif self.proximity >= 10:
                self.proximity -= 2
            print("Proximity to nearby vehicle is :{} metres\n".format(self.proximity))
           

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
            time.sleep(3)
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
        while True:
            result = random.randint(-70, 70)
            self.angle = result
            print("Direction in which vehicle is heading:{}\n".format(self.angle))
            time.sleep(8)

    def get_direction(self):
        return str(self.angle)

class TemperatureSensor(Sensor):
    def __init__(self, sensor_name) -> None:
        super().__init__(sensor_name)
        self.temperature = 68
    
    def change_temp(self):
        while True:
            time.sleep(3)
            result = random.randint(0, 2)
            if result == 1:
                self.temperature += random.randint(0,70)
            else:
                self.temperature -= random.randint(0,10)
            print("Temperature of engine is :{} degree celcius\n".format(self.temperature))

    def generate_data(self):
        t1 = threading.Thread(target=self.change_temp)
        t1.start()
        time.sleep(1)

    def get_temperature(self):
        return str(self.temperature)

class PressureSensor(Sensor):
    def __init__(self, sensor_name)->None:
        super().__init__(sensor_name)
        self.pressure = 35
    
    def change_pressure(self):
        while True:
            time.sleep(3)
            result = random.randint(0, 18)
            self.pressure = self.pressure - result
            if self.pressure < 10:
                self.pressure += 30
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


class CarGear(Sensor):
    def __init__(self, sensor_name)->None:
        super().__init__(sensor_name)
        self.gear = 0

    def change_gear(self):
        while True:
            time.sleep(3)
            new_load = random.randint(0,6)
            self.gear+= new_load
            if self.gear>6:
                self.gear = 6
            print("Car running on gear {} \n".format(self.gear))
            time.sleep(7)
    

    def generate_data(self):
        t1 = threading.Thread(target=self.change_gear)
        t1.start()

    def get_gear(self):
        return str(self.gear)

class CarPetrol(Sensor):
    def __init__(self, sensor_name)->None:
        super().__init__(sensor_name)
        self.petrol = 10

    def change_petrol(self):
        while True:
            time.sleep(3)
            petrol_spent = random.randint(0,5)
            self.petrol -= petrol_spent
            if self.petrol == 0:
                self.petrol = 15
            print("Current petrol in the car {} litres \n".format(self.petrol))
            time.sleep(4)
    

    def generate_data(self):
        t1 = threading.Thread(target=self.change_petrol)
        t1.start()

    def get_petrol(self):
        return str(self.petrol)

class PeopleInCar(Sensor):
    def __init__(self, sensor_name)->None:
        super().__init__(sensor_name)
        self.number = 5

    def change_passenger(self):
        while True:
            time.sleep(3)
            people = random.randint(0,4)
            self.number -= people
            if self.number <=0:
                self.number = 5
            print("Number of passengers in the car {} \n".format(self.number))
            time.sleep(4)

    def generate_data(self):
        t1 = threading.Thread(target=self.change_passenger)
        t1.start()

    def get_passenger(self):
        return str(self.number)

class AirCondition(Sensor):
    def __init__(self, sensor_name)->None:
        super().__init__(sensor_name)
        self.ac_temperature = 23

    def change_temp(self):
        while True:
            time.sleep(3)
            temp = random.randint(0,10)
            self.ac_temperature -= temp
            if self.ac_temperature <0:
                self.ac_temperature = 30
            print("Temperature of air condition {} \n".format(self.ac_temperature))

    def generate_data(self):
        t1 = threading.Thread(target=self.change_temp)
        t1.start()

    def get_ac_temp(self):
        return str(self.ac_temperature)




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



