import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta
import time

# time_start = time.time()


parser = argparse.ArgumentParser(
    prog="ExchangeRate",
    description="Exchange rate for EUR to UAH and USD to UAH")

parser.add_argument("n", metavar="amount_of_days", type=int, choices=range(1, 11))
args = parser.parse_args()

URL = "https://api.privatbank.ua/p24api/exchange_rates"


async def get_exchange_rates(url: str, date: str):
    
    params = {
        "json": "",
        "date": date}
    
    async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:

                # print("Status:", response.status)
                # print("Content-type:", response.headers['content-type'])
                # print('Cookies: ', response.cookies)
                # print(response.ok)
                exchanges = await response.json()
                
                # print(f"{date=}, time={time.time() - time_start}")
    
    return [exchange for exchange in exchanges["exchangeRate"]
        if exchange["currency"] == "EUR" or exchange["currency"] == "USD"]
    
    
async def main():
    
    date_now = datetime.now()    
    futures = []
    
    for i in range(args.n):
        
        delta = timedelta(days=i)        
        date = date_now - delta
        date_str = date.strftime("%d.%m.%Y")
        futures.append(get_exchange_rates(URL, date_str))
       
    return await asyncio.gather(*futures)


if __name__ == "__main__":
    # time_now = time.time()
    results = asyncio.run(main())
    
    # print(time.time() - time_now)
    
    for result in results:
        print(result)
        
    # print(time.time() - time_now)
        