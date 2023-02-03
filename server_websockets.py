import asyncio
from aiofile import async_open
from aiopath import AsyncPath
from datetime import datetime
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
import json

import exchange.exchange as exchange


LOGGING = AsyncPath("logging.txt")


class Server:
        
    async def ws_handler(self, ws: WebSocketServerProtocol):
        
        try:
            await self.exchange_handler(ws)            
        except ConnectionClosedOK:
            pass
            
    async def exchange_handler(self, ws: WebSocketServerProtocol):
        
        async for message in ws:
            await ws.send(json.dumps(["Wait..."]))
            
            n = 1
            currency = None
            
            if len(message.split()) == 1:
                command = message
                
            elif len(message.split()) == 2:
                command, n = message.split()
                
            elif len(message.split()) == 3:
                command, n, currency = message.split()                
           
            if command == "exchange":
                async with async_open(LOGGING, "a") as afd:
                    await afd.write(
                        f"Exchange: {datetime.now()}, days: {n}, additional currency: {currency}\n"
                    )
                    
                exchanges = await (exchange.main(int(n), currency))
                message = await self.table_for_exchanges(exchanges)
                
            else:
                message = ["I don`t know this command"]
                
            await ws.send(json.dumps(message))
            

    async def table_for_exchanges(self, exchanges):
        
        template = "|{:.^10}|{:.^10}|{:.^10}|{:.^10}|"
        headers = ["Date", "Currency", "Sale", "Purchase"]
        header = template.format(*headers)
        dividing_line = "|" + "-" * 43 + "|"
        
        table = [dividing_line, header, dividing_line]
        
        for exchange in exchanges:
            for date, values in exchange.items():
                for currency, rates  in values.items():
                        
                    table.append(template.format(date, currency, rates["sale"], rates["purchase"]))
                    date = ""
                        
            table.append(dividing_line)
        
        return table


async def main():    
    server = Server()
    
    async with websockets.serve(server.ws_handler, "0.0.0.0", 8080):
        await asyncio.Future()
        

if __name__ == "__main__":
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass 