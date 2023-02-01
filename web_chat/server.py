import asyncio
import logging
import names
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.DEBUG)


class Server:
    clients = set()
    
    async def register(self, ws: WebSocketServerProtocol):
        
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")
        
    async def unregister(self, ws: WebSocketServerProtocol):
        
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")
        
    async def send_to_clients(self, messange: str):
        
        if self.clients:
            [await client.send(messange) for client in self.clients]
        
    async def ws_handler(self, ws: WebSocketServerProtocol):
        
        await self.register(ws)
        
        try:
            await self.distrubute(ws)
            
        except ConnectionClosedOK:
            pass
        
        finally:
            await self.unregister(ws)
            
    async def distrubute(self, ws: WebSocketServerProtocol):
        
        async for message in ws:
            await self.send_to_client(f"{ws.name}: {message}")
            

async def main():
    
    server = Server()
    
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()
        

if __name__ == "__main__":
    asyncio.run(main())
