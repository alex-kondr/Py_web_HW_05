import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta


parser = argparse.ArgumentParser(
    prog="ExchangeRate",
    description="Exchange rate for EUR to UAH and USD to UAH")

parser.add_argument("-d", "--days", metavar="Amount of days", type=int, choices=range(1, 11))
parser.add_argument("-c", "--choice", metavar="Choice currency (Example: -c AUD)", type=str)
args = parser.parse_args()


def parse_exchanges(exchanges):
    
    date = exchanges["date"]  
    exchange_by_date = {date: {}}

    for exchange in exchanges["exchangeRate"]:
        if (
            exchange["currency"] == "EUR" or 
            exchange["currency"] == "USD" or 
            exchange["currency"] == args.choice
        ):            
            exchange_by_date[date].update(
                {
                    exchange["currency"]: {                        
                        "sale": exchange["saleRateNB"],
                        "purchase": exchange["purchaseRateNB"]
                    }
                }
            )
            
    return exchange_by_date


async def main():
    
    base_url = "https://api.privatbank.ua/p24api/exchange_rates"
    date_now = datetime.now()
    
    result = []
    
    async with aiohttp.ClientSession() as session:        
        for i in range(args.days):
            
            date = date_now - timedelta(days=i)
            date_str = date.strftime("%d.%m.%Y")
            
            params = {
                "json": "",
                "date": date_str
            }
            
            try:
                async with session.get(base_url, params=params) as response:                
                    
                    if response.status == 200:
                        
                        exchanges = await response.json()
                        exchange_by_date = parse_exchanges(exchanges)
                        result.append(exchange_by_date)
                        
                    else:
                        print(f"Error status: {response.status} for '{base_url}' params={params}")
                
            except aiohttp.ClientConnectionError as error:
                print(f"{str(error)}")
            
    return result


if __name__ == "__main__":
    
    print(asyncio.run(main()))