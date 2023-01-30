import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta





parser = argparse.ArgumentParser(
    prog="ExchangeRate",
    description="Exchange rate for EUR to UAH and USD to UAH")

parser.add_argument("n", metavar="amount_of_days", type=int)

args = parser.parse_args()
# print(args.n)

# quit()

URL = "https://api.privatbank.ua/p24api/exchange_rates"

# async def 


async def get_exchange_rates(url: str, date: str):
    
    params = {
        "json": "",
        "coursid": date}
    
    async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:

                # print("Status:", response.status)
                # print("Content-type:", response.headers['content-type'])
                # print('Cookies: ', response.cookies)
                # print(response.ok)
                result = await response.json()
                
                print(f"{result=}")
                
                return result

async def main():
    
    date_now = datetime.now()
    
    for _ in range(args.n):
        
        delta = timedelta(days=1)        
        date = date_now - delta
        date_str = date.strftime("%d.%m.%Y")
        
        print(f"{date_str=}")
    
        result = await get_exchange_rates(URL, date_str)
       
    return result
    

    


if __name__ == "__main__":
    # if platform.system() == 'Windows':
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)