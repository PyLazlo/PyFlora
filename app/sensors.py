from random import uniform, randint
from .database import Data
from .api import get_data_from_url
import datetime

class RaspberryPiSim:
    def __init__(self):
        self.temp = Sensor(name = "Temperature", rand_min= -5, rand_max= 45)
        self.hydration = Sensor(name = "Hydration", rand_min= 0, rand_max= 100)
        self.pH = Sensor(name = "pH", rand_min= 0, rand_max= 14)
        self.light = Sensor(name = "Light", rand_min= 0, rand_max= 2)
        


    
    def send_data(self, pot_id, plant_id):
        """
        Class method that returns Data object used for adding
        sensor readings to the database
        @params
        pot_id
        plant_id
        """
        data=Data()
        data.sen_temp = self.temp.generate_random_value()
        data.sen_pH = self.pH.generate_random_value()
        data.sen_hydration = self.hydration.generate_random_value()
        data.sen_light = self.light.generate_random_light()
        data.sen_date = datetime.datetime.now()
        data.pot_id = pot_id
        data.plant_id = plant_id
        data.api_temp = get_data_from_url()
        return data
    
    
    

class Sensor:
    def __init__(self, name, rand_min, rand_max):
        self.name = name
        self.rand_max = rand_max
        self.rand_min = rand_min
        

    def generate_random_value(self):
        """
        Class method used to generate a random float value
        for sensors reading simulation
        """
        return round(uniform(self.rand_min, self.rand_max), 2)
        
    def generate_random_light(self):
        """
        Class method used to generate a random integer value
        used as index for a list of strings representing the sensors reading
        """
        list = ["High", "Mid", "Low"]
        return list[randint(self.rand_min, self.rand_max)]
  

