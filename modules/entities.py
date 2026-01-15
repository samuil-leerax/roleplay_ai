
import modules.InfoLoader as infload

class CharacterEntity:
    def __init__(self, character_data : infload.Character):
        self.character_data = character_data
        self.current_memory = []
        self.current_state = ""
        self.inventory = []
        
        self.position = {
            "location": None,
            "coordinates": (0,0)
        }
    
class LocationEntity:
    def __init__(self, location_data : infload.Location):
        self.location_data = location_data
        self.chat_history = []
        self.current_state = ""

class WorldEntity:
    def __init__(self, world_description: str):
        self.world_description = world_description
        self.current_state = ""
        self.current_time = {
            "date": "0000-00-00",
            "time": "00:00"
        }