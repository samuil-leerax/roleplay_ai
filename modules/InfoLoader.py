import json
import os


class Character:
    def __init__(self, file_path):
        # Initialize variables to store character data
        self.name = ""
        self.race = ""
        self.age = ""
        self.gender = ""
        self.role = ""
        self.species_type = ""
        
        self.visual_description = ""
        self.personality = ""
        self.memory = []
        self.sequential_memory = []
        self.long_memory = []
        
        # Parse data from file
        self._load_from_file(file_path)
    
    def _load_from_file(self, file_path):
        """Parse character data from JSON file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Character file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Parse description fields
        description = data.get("Description", {})
        self.name = description.get("name", "")
        self.race = description.get("race", "")
        self.age = description.get("age", "")
        self.gender = description.get("gender", "")
        self.role = description.get("role", "")
        self.species_type = description.get("species_type", "")
        
        # Parse visual description and personality
        self.visual_description = data.get("Visual Description", "")
        self.personality = data.get("Personality", "")
        
        # Parse memory arrays
        self.memory = data.get("Memory", [])
        self.sequential_memory = data.get("Sequential_Memory", [])
        self.long_memory = data.get("Long_Memory", [])
        
        


class Location:
    def __init__(self, file_path):
        # Initialize variables to store location data
        self.name = ""
        self.description = ""
        
        # Parse data from file
        self._load_from_file(file_path)
    
    def _load_from_file(self, file_path):
        """Parse location data from JSON file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Location file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Parse location fields
        self.name = data.get("Name", "")
        self.description = data.get("Description", "")
        
        


class World:
    def __init__(self, file_path):
        # Initialize variables to store world data
        self.name = ""
        self.description = ""
        
        # Parse data from file
        self._load_from_file(file_path)
    
    def _load_from_file(self, file_path):
        """Parse world data from JSON file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"World file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Parse world fields
        self.name = data.get("Name", "")
        self.description = data.get("Description", "")
        
        