import prompt_builder
from openrouter import OpenRouter
import os
import prompt_builder
import test_characters



class Session:
    def __init__(self, api_key,world: prompt_builder.WorldPrompt):
        self.world = world
        self.chat_history = []
        self.independent_chat = []
        self.client = OpenRouter(api_key=api_key)
    
    def send_request(self, model):
        stream = self.client.chat.send(
            model=model,  
            messages=self.chat_history,
            temperature=1,
            stream=True,     
        )
        return(stream)