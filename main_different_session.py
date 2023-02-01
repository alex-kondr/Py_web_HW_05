import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta
import platform
import time

time_start = time.time()


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
                if not response.ok:
                    return response.ok
                    # return "The site does not respond or the request is not valid"
                    
                exchanges = await response.json()
                
                print("time session:", time.time() - time_start)
                
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
            
    return result
    
    # return [exchange for exchange in exchanges["exchangeRate"]
    #     if exchange["currency"] == "EUR" or exchange["currency"] == "USD"]
    
    
async def run_futures():
    
    date_now = datetime.now()    
    futures = []
    
    for i in range(args.n):
        
        delta = timedelta(days=i)        
        date = date_now - delta
        date_str = date.strftime("%d.%m.%Y")
        futures.append(get_exchange_rates(URL, date_str))
        
        # if 
       
    # return [results[0] for results in await asyncio.gather(*futures)]
    return await asyncio.gather(*futures)
    
    # return result


def main():
    results = asyncio.run(run_futures())
    
    if not results[0]:
        return "The site does not respond or the request is not valid"
    
    return results
    
    # for result in results:
    #     print(result)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    
    print(main())
    
    print("total:", time.time() - time_start)
    
    
    # time_now = time.time()
    
    # print(time.time() - time_now)
    
    # for result in results:
    #     print(result)
        
    # print(time.time() - time_now)
        