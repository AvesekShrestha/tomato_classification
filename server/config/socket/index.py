from fastapi import WebSocket

class SocketManager : 

    def __init__(self) :
        self.active_connections : dict[int, WebSocket] = {}

    async def connect(self, user_id : int, socket : WebSocket) : 
        await socket.accept()
        self.active_connections[user_id] = socket

    async def disconnect(self, user_id : int) : 
        self.active_connections.pop(user_id)

    async def send_message(self, to : int, message : str) :
        socket : WebSocket | None = self.active_connections.get(to)
        if socket :
            await socket.send_text(message)
