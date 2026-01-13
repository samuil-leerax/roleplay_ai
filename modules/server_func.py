# -*- coding: utf-8 -*-
from fastapi import WebSocket
import json





# Function to format messages before sending to clients
def send_formatting(action, content):
    return(json.dumps({"action": action, "content": content}, ensure_ascii=False))


# Function to broadcast message to all connected clients
async def broadcast_message(message: str, active_connections: list[WebSocket]):
    """Отправка сообщения всем подключенным клиентам"""
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            disconnected.append(connection)
    
    # Удаляем отключенные соединения
    for connection in disconnected:
        active_connections.remove(connection)
        
# Function to broadcast message to all connected clients except one
async def broadcast_message_withexception(message: str, exception: WebSocket, active_connections: list[WebSocket]):
    """Отправка сообщения всем подключенным клиентам, кроме указанного исключения"""
    disconnected = []
    for connection in active_connections:
        if connection == exception:
            continue  # Пропускаем исключение
        try:
            await connection.send_text(message)
        except Exception:
            disconnected.append(connection)
    
    # Удаляем отключенные соединения
    for connection in disconnected:
        active_connections.remove(connection)
