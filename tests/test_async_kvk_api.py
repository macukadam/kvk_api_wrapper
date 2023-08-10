"""
An example test case with pytest and pytest-asyncio.
See: https://pytest-asyncio.readthedocs.io/
"""
import pytest
from kvk_api_client.async_client import KVK
from kvk_api_client.paths import BasisProfielPaths

KVK_NUMBER = '68750110'
VESTIGINGSNUMMER = '000038509504'


@pytest.mark.asyncio
async def test_get_basis_profile():
    async with KVK(test=True) as kvk:
        response = await kvk.get_basis_profiel(KVK_NUMBER)
        assert response.status == 200

        response = await kvk.get_basis_profiel(KVK_NUMBER, BasisProfielPaths.vestigingen)
        assert response.status == 200

        response = await kvk.get_basis_profiel(KVK_NUMBER, BasisProfielPaths.eigenaar)
        assert response.status == 200

        response = await kvk.get_basis_profiel(KVK_NUMBER, BasisProfielPaths.hoodfvestiging)
        assert response.status == 200

@pytest.mark.asyncio
async def test_get_vestigingsprofiel():
    async with KVK(test=True) as kvk:
        response = await kvk.get_vestigingsprofiel(VESTIGINGSNUMMER)
        assert response.status == 200

@pytest.mark.asyncio
async def test_get_companies():
    async with KVK(test=True) as kvk:
        response = await kvk.get_companies(kvk_number=KVK_NUMBER)
        assert response.status == 200

@pytest.mark.asyncio
async def test_get_naamgevingen():
    async with KVK(test=True) as kvk:
        response = await kvk.get_naamgevingen(kvk_number=KVK_NUMBER)
        assert response.status == 200

