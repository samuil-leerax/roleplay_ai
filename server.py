# -*- coding: utf-8 -*-
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import modules.session as session
import modules.server_func as sf
import keys
import temp_modules.test_characters as test_characters
import temp_modules.example_session as example_session
import json
import traceback

app = FastAPI()
session_instance = example_session.session_instance
model = keys.deepseek_v3_2

# Список активных WebSocket соединений
active_connections: list[WebSocket] = []

# Init Current settings
curr_charcter = test_characters.test_char
curr_world = test_characters.test_world
curr_player = test_characters.test_player
curr_location = test_characters.test_location

full_character_list = [test_characters.test_char, test_characters.test_char2]




curr_id = 0

class SendMessageHandler:
    def __init__(self):
        pass
    
    def session_handle(self, user_message: str, user_character: str):
        session_instance.locations[curr_location.name].independent_chat_history.append({"name": user_character, "content": user_message}) # Add user message to location independent chat history
        stream, character_name = session_instance.proceed_forward(curr_location.name, full_character_list) # Proceed forward in session
        return stream, character_name
    
    async def handle(self, streaming_id, data_json, ws: WebSocket):
        
        # Extracting data from response
        datas = json.loads(data_json.get("data", "")) # Extract data JSON
        message, character = datas.get("message", ""), datas.get("character", "") # Extract message and character
        
        # Broadcast initial message to all clients
        
        
        # Handling session
        stream, character_name = self.session_handle(message, character)
        
        # Message initialization for client streaming
        
        init_response = {"name": character_name, "id": streaming_id, "picture_url": "https://picsum.photos/150"}
        await sf.broadcast_message_withexception(sf.send_formatting("user_message_broadcast", json.dumps({"name": character, "message": message}, ensure_ascii=False)), ws, active_connections)
        await sf.broadcast_message(sf.send_formatting("prompt_response_init", json.dumps(init_response, ensure_ascii=False)), active_connections)
        
        # Streaming
        
        full_response = "" # Variable to store full response
        
        for chunk in stream:
            delta = chunk.choices[0].delta # Extract delta from stream chunk
            if hasattr(delta, 'content') and delta.content: # Check if content exists in delta
                content = delta.content # Extract content
                full_response += content # Append content to full response
                
                response = {"id": streaming_id, "message": content} # Prepare response before sending to client
                
                await sf.broadcast_message(sf.send_formatting("prompt_response", json.dumps(response, ensure_ascii=False)), active_connections) # Send AI response chunks for all connected clients
        await sf.broadcast_message(sf.send_formatting("prompt_response", json.dumps({"id": streaming_id, "message": "[END]"}, ensure_ascii=False)), active_connections)  # Notify clients that response is complete
        
        # Applying response to chat histories
        session_instance.locations[curr_location.name].independent_chat_history.append({"name": character_name, "content": full_response}) # Add assistant/character's message to independent chat
        
    


# Function to write data based on address
def write_data_by_address(address, data):
    if(address == "character/name"):
        curr_charcter.name = data
    elif(address == "character/description"):
        curr_charcter.description = data
    elif(address == "character/personality"):
        curr_charcter.personality = data
    elif(address == "character/current_memory"):
        curr_charcter.current_memory = data
    elif(address == "world/description"):
        curr_world.description = data
    elif(address == "world/const_rules"):
        curr_world.const_rules = data
    elif(address == "player/name"):
        curr_player.name = data
    elif(address == "player/visual_description"):
        curr_player.visual_description = data
    

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    # Message acceptance
    await ws.accept() # Accept connection
    active_connections.append(ws) # Append new connection
    
    try:
        while True:
            
            # Receiving and processing data from client
            data = await ws.receive_text() # Receive data
            data_json = json.loads(data) # Parse JSON
            print("Received data:", data_json) # Log received data

            
            # Send message action (Action which triggers response generation)
            
            if(data_json.get("action") == "send_message"):
                curr_handler = SendMessageHandler() # Initialize message handler
                # Message initialization for client streaming
                
                global curr_id # Curr message ID
                curr_id += 1 # Increment ID
                streaming_id = curr_id # Making ID local for this stream
                
                await curr_handler.handle(streaming_id, data_json, ws) # Handle message
                
            
            if(data_json.get("action") == "receive_data"):
                
                data_output = [
                    {"data_title": "world", "data_content": [{"data_title": "description", "data_content": curr_world.description}, {"data_title": "const_rules", "data_content": curr_world.const_rules}]},
                    {"data_title": "character", "data_content": [{"data_title": "name", "data_content": curr_charcter.name}, {"data_title": "description", "data_content": curr_charcter.description}, {"data_title": "personality", "data_content": curr_charcter.personality}, {"data_title": "current_memory", "data_content": curr_charcter.current_memory}]},
                    {"data_title": "player", "data_content": [{"data_title": "name", "data_content": curr_player.name}, {"data_title": "visual_description", "data_content": curr_player.visual_description}]}
                ]
                await ws.send_text(sf.send_formatting("receive_data", json.dumps(data_output, ensure_ascii=False)))
                
            # Send data action (Action which updates internal data based on client input)
            
            if(data_json.get("action") == "send_data"):
                
                data_to_process = json.loads(data_json.get("data", "")) # Extract data to process
                
                # Process each data item
                
                for item in data_to_process:
                    address = item.get("address", "")
                    content = item.get("content", "")
                    write_data_by_address(address, content) # Write data based on address
            
            # Send full history action (Send all chat history to the new client)
            if(data_json.get("action") == "get_full_history"):
                await ws.send_text(sf.send_formatting("full_history", json.dumps(session_instance.locations.get(curr_location.name).independent_chat_history, ensure_ascii=False)))
    
    # Handling disconnection
    except WebSocketDisconnect:
        # Delete connection from active connections
        if ws in active_connections:
            active_connections.remove(ws)
        print("Client disconnected")
    except Exception as e:
        # Delete connection from active connections on error
        if ws in active_connections:
            active_connections.remove(ws)
        print(f"Error in websocket: {e}")
        print(f"Traceback:\n{traceback.format_exc()}")
            