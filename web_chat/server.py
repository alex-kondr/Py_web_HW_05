import asyncio
import logging
import names
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

import exchange


logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()
    
    async def register(self, ws: WebSocketServerProtocol):            
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address}, {ws.name=} connects")
        
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
            
            n = 1
            currency = None
            
            if len(message.split()) == 1:
                command = message
                
            elif len(message.split()) == 2:
                command, n = message.split()
                
            elif len(message.split()) == 3:
                command, n, currency = message.split()                
           
            if command == "exchange":
                exchanges = await (exchange.main(int(n), currency))
                message = await table_for_exchanges(exchanges)
                
            await self.send_to_clients(str(message))
            

async def table_for_exchanges(exchanges):
    
    template = "\n<br>|{:^10}|{:^10}|{:^10}|{:^10}|"
    headers = ["Date", "Currency", "Sale", "Purchase"]
    header = template.format(*headers)
    dividing_line = "\n<br>|" + "-" * 43 + "|"
    
    table = dividing_line + header + dividing_line
    
    for exchange in exchanges:
        for date, values in exchange.items():
            for currency, rates  in values.items():
                    
                table += template.format(date, currency, rates["sale"], rates["purchase"])
                date = ""
                    
        table += dividing_line
    
    return table


async def main():
    
    server = Server()
    
    async with websockets.serve(server.ws_handler, "0.0.0.0", 8080):
        await asyncio.Future()
        

if __name__ == "__main__":
    
    # a = asyncio.run(exchange.main())
    # print(f"{a=}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass 
