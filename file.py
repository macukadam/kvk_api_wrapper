import asyncio
from kvk_api_client import AsyncKVK


KVK_NUMBER = "68750110"


async def get_basis_profiel():
    async with AsyncKVK(test=True) as kvk:
        profiel = await kvk.get_basis_profiel(KVK_NUMBER)
        print(await profiel.json())


asyncio.run(get_basis_profiel())

