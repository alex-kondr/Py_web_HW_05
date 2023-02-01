import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta
import platform


parser = argparse.ArgumentParser(
    prog="ExchangeRate",
    description="Exchange rate for EUR to UAH and USD to UAH")

parser.add_argument("n", metavar="amount_of_days", type=int, choices=range(1, 11))
args = parser.parse_args()

URL = "https://api1.privatbank.ua/p24api/exchange_rates"


def get_urls(n: int) -> list[str]:
    
    urls = []    
    date_now = datetime.now() 
    
    for i in range(n):
        
        delta = timedelta(days=i)        
        date = date_now - delta
        date_str = date.strftime("%d.%m.%Y")
        urls.append(f"{URL}?json&date={date_str}")
    
    return urls


async def get_exchange_rates(urls: list[str]):
    
    result = []
    
    async with aiohttp.ClientSession() as session:        
        for url in urls:
            
            try:
                async with session.get(url) as response:                
                    
                    if response.status == 200:                        
                        exchanges = await response.json()
                        
                    else:
                        return f"Error status: {response.status} for {url}"
                
            except aiohttp.ClientConnectionError as error:
                return {str(error)}
            
            date = exchanges["date"]  
            exchange_by_date = {date: {}}
    
            for exchange in exchanges["exchangeRate"]:
                if exchange["currency"] == "EUR" or exchange["currency"] == "USD":
                    exchange_by_date[date].update(
                        {
                            exchange["currency"]: {                        
                                "sale": exchange["saleRate"],
                                "purchase": exchange["purchaseRate"]
                            }
                        }
                    )
                    
            result.append(exchange_by_date)
            
    return result


def main():
    
    urls = get_urls(args.n)
    results = asyncio.run(get_exchange_rates(urls))
    
    return results


if __name__ == "__main__":
    
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    
    print(main())