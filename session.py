import prompt_builder
from openrouter import OpenRouter
import openai
import keys
import os
import prompt_builder
import test_characters
import json
import ast

class LocationData:
    def __init__(self, location_prompt: prompt_builder.LocationPrompt, client):
        self.location_prompt = location_prompt
        self.independent_chat_history = []
        self.characters_in_location = [] # {"position": (x,y), "character": character_instance}
        self.player_characters_in_location = [] # {"position": (x,y), "character": player_instance}
        self.client = client
        
    def add_character(self, character_instance, position):
        self.characters_in_location.append({"position": position, "character": character_instance.name})
    
    def add_player_character(self, player_instance, position):
        self.player_characters_in_location.append({"position": position, "character": player_instance.name})
    
    def remove_character(self, character_instance):
        self.characters_in_location = [c for c in self.characters_in_location if c["character"] != character_instance.name]
    
    async def choose_character_to_talk(self, full_character_list):
        prompt_1_sys = (
            "You are system that make list of possible characters to start talking\n"
            "you will get list of characters with their positions in location the location\n"
            "Also you will get 10 last message of diaglog in location to understand context and choose the most relevant character to start talking\n"
            "You will not add player characters to output, they are needed for context only\n"
            
            
            "HERE IS YOUR OUTPUT FORMAT (MUST BE VALID JSON WITH DOUBLE QUOTES):\n"
            '[{"position": [x,y], "character_name": "name of character to start talking"}, ...]\n'
        )
        
        prompt_1_user = (
            "Here is characters with their positions:\n"
            f"{json.dumps(self.characters_in_location, indent=2)}\n"
            "Here is player characters with their positions:\n"
            f"{json.dumps(self.player_characters_in_location, indent=2)}\n"
            "Here is last 10 messages in diaglog in location:\n"
            f"{json.dumps(self.independent_chat_history[-10:], indent=2)}\n"
        )
        
        prompt_1 = [
            {"role": "system", "content": prompt_1_sys},
            {"role": "user", "content": prompt_1_user}
        ]
        response = self.client.chat.send(
            model=keys.qwen3_235b_instruct,  
            messages=prompt_1,
            temperature=0,
            stream=False,     
        )
        
        response_text = response.choices[0].message.content
        json_output = None
        try:
            json_output = json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, try Python literal evaluation
            try:
                json_output = ast.literal_eval(response_text)
            except (ValueError, SyntaxError) as e:
                print(f"Failed to parse response: {e}")
                return []
        print(response_text)
        
        
        prompt_2_system = (
            "You are system that choose one character from list to start talking based on context of diaglog, characters descriptions and other info that user will provide\n"
            "You will get list of characters with their positions in location\n"
            "HERE IS YOUR OUTPUT FORMAT (MUST BE VALID JSON WITH DOUBLE QUOTES):\n"
            '{"character_name": "name of character to start talking"}\n'
        )
        
        prompt_2_user = ""
        
        for char_info in json_output:
            char_name = char_info.get("character_name", "")
            for char in full_character_list:
                if(char.name == char_name):
                    character_instance = char
                    prompt_2_user += (
                        f"Character name: {char_name}\n"
                        f"Character description: {character_instance.description}\n"
                        f"Character current memory: {character_instance.current_memory}\n"
                        f"Character visual description: {character_instance.visual_description}\n"
                        "----\n"
                    )
        prompt_2_user += (
            "Here is full chat history in location:\n"
            f"{json.dumps(self.independent_chat_history, indent=2)}\n"
        )
        
        prompt_2 = [
            {"role": "system", "content": prompt_2_system},
            {"role": "user", "content": prompt_2_user}
        ]
        
        response_2 = self.client.chat.send(
            model=keys.qwen3_235b_instruct,  
            messages=prompt_2,
            temperature=0,
            stream=False,     
        )
        response_text2 = response_2.choices[0].message.content
        json_output2 = None
        try:
            json_output2 = json.loads(response_text2)
        except json.JSONDecodeError:
            # If JSON parsing fails, try Python literal evaluation
            try:
                json_output2 = ast.literal_eval(response_text2)
            except (ValueError, SyntaxError) as e:
                print(f"Failed to parse response: {e}")
        
        print(response_text2)
        
        # Try to parse as JSON first, fallback to ast.literal_eval for Python syntax
        

class Session:
    def __init__(self, api_key,world: prompt_builder.WorldPrompt):
        self.world = world
        self.locations = {}
        self.characters = {}
        ## TODO Change some how structure to work with multiple characters and locations
        self.chat_history = []
        self.independent_chat = []
        self.client = OpenRouter(api_key=api_key)
        self.client_deepseek = openai.OpenAI(api_key=keys.api_key_deepseek, base_url="https://api.deepseek.com")
    
    def add_character(self, character_prompt: prompt_builder.CharacterPrompt):
        self.characters[character_prompt.name] = character_prompt
        
    def add_location(self, location_prompt: prompt_builder.LocationPrompt, client):
        self.locations[location_prompt.name] = LocationData(location_prompt, client)
        
    def add_character_to_location(self, character_name, location_name, position):
        if(location_name in self.locations and character_name in self.characters):
            self.locations[location_name].add_character(self.characters[character_name], position)
    
## Models requests functions
    def send_request(self, model):
        stream = self.client.chat.send(
            model=model,  
            messages=self.chat_history,
            temperature=1,
            stream=True,     
        )
        return(stream)
    def send_request_deepseekchat(self):
        stream = self.client_deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=self.chat_history,
        temperature=1,
        stream=True
        )
        return(stream)