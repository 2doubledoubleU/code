import httpx
import asyncio

a = asyncio.run(httpx.get('https://www.deviantart.com/rook-07/art/Kinktober-2019-day-13-Glue-821381324'))
print(a)