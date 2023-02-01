import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta
import platform
import time


# start_time = time.time()

parser = argparse.ArgumentParser(
    prog="ExchangeRate",
    description="Exchange rate for EUR to UAH and USD to UAH")

parser.add_argument("n", metavar="amount_of_days", type=int, choices=range(1, 11))
args = parser.parse_args()

URL = "https://api1.privatbank.ua/p24api/exchange_rates"


async def get_exchange_rates(session, url: str, date: str):
    
    params = {
        "json": "",
        "date": date}
    
    async with session.get(url, params=params) as response:
        
        if not response.ok:
            return response.ok
            
        exchanges = await response.json()
                
                # print(f"{date=}, {exchanges=}")
                
    result = {date: {}}
    
    for exchange in exchanges["exchangeRate"]:
        if exchange["currency"] == "EUR" or exchange["currency"] == "USD":
            result[date].update(
                {
                    exchange["currency"]: {                        
                        "sale": exchange["saleRate"],
                        "purchase": exchange["purchaseRate"]
                    }
                }
            )
    
    # print("time session:", time.time() - start_time)
            
    return result


async def run_futures():
    
    date_now = datetime.now()    
    futures = []
    
    async with aiohttp.ClientSession() as session:
    
        for i in range(args.n):
            
            delta = timedelta(days=i)        
            date = date_now - delta
            date_str = date.strftime("%d.%m.%Y")
            futures.append(get_exchange_rates(session, URL, date_str))
        
        return await asyncio.gather(*futures)
    

def main():
    
    results = asyncio.run(run_futures())
    
    if not results[0]:
        return "The site does not respond or the request is not valid"
    
    return results


if __name__ == "__main__":
    
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())    
    
    print(main())
    
    print("time: ", time.time() - start_time)
    