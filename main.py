import aiohttp
import asyncio
import argparse


parser = argparse.ArgumentParser(
    prog="ExchangeRate",
    description="Exchange rate for EUR to UAH and USD to UAH")

parser.add_argument("amount_of_days", metavar="n", type=int)

args = parser.parse_args()
print(args.amount_of_days)

quit()

URL = "https://api.privatbank.ua/p24api/exchange_rates"


async def main():
    
    params = {
        "json": "",
        "coursid": "5"}

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.privatbank.ua/p24api/pubinfo", params=params) as response:

            # print("Status:", response.status)
            # print("Content-type:", response.headers['content-type'])
            # print('Cookies: ', response.cookies)
            # print(response.ok)
            result = await response.json()
            return result


if __name__ == "__main__":
    # if platform.system() == 'Windows':
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)