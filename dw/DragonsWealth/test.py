import asyncio
import tinvest

TOKEN = "<TOKEN>"


async def main():
    client = tinvest.AsyncClient(TOKEN)
    response = await client.get_portfolio()  # tinvest.PortfolioResponse
    print(response.payload)

    await client.close()

asyncio.run(main())