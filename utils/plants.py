import json

def load_plants(path='assets/plants.json'):
    with open(path) as plants_file:
        return json.load(plants_file)

class Plants:
    def get_plant(self, plant_name):
        plants = load_plants()
        return plants.get(plant_name, None)