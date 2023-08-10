"""A very simple wrapper around KVK api."""

import warnings
import os
import aiohttp
from dotenv import load_dotenv
from typing import Optional
from kvk_api_client.paths import APIpaths

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
load_dotenv()

class KVK:
    """
    A class for interacting with the KVK API.

    Args:
    -----------
    test (bool): If True, uses the KVK API test environment.

    Raises:
    -----------
    ValueError: If the required environment variables are not set.

    Attributes:
    -----------
    host (str): The KVK API host URL.

    api_version (str): The KVK API version.

    api_key (str): The API key for authentication.

    headers (dict): HTTP headers for API requests.

    Example usage:
    -----------
        >>> kvk = KVK(test=True)
        >>> response = await kvk.get_basis_profiel('12345678')
    """

    def __init__(self, test: bool) -> None:
        self.host = os.getenv('KVK_HOST')
        self.api_version = os.getenv('KVK_API_VERSION')
        self.api_key = os.getenv('KVK_APIKEY_PROD')

        if not self.host:
            raise ValueError('KVK_HOST is not set')

        if not self.api_version:
            raise ValueError('KVK_API_VERSION is not set')

        if not self.api_key:
            raise ValueError('KVK_APIKEY is not set')

        if test:
            self.api_key = os.getenv('KVK_APIKEY_TEST')
            self.api_version = 'test/' + self.api_version

        if not self.api_key:
            raise ValueError('KVK_APIKEY is not set')

        self.headers = {'apikey': self.api_key}
        self.session = None


    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers,
                                         connector=aiohttp.TCPConnector(
                                             ssl=False))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


    async def __send_request(self, method: str, path: str, **kwargs) -> aiohttp.ClientResponse:
        """Send an HTTP request to the KVK API."""
        url = f"{self.host}/{self.api_version}/{path}"
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if method == "GET":
            response = await self.session.get(url, params=kwargs)
        elif method == "POST":
            response = await self.session.post(url, data=kwargs)
        else:
            raise ValueError('Only GET and POST methods are supported.')

        return response


    async def get_basis_profiel(self, kvk_number: str,
                                basis_profile_type: Optional[str] = None,
                                geo_data: str = "False") -> aiohttp.ClientResponse:
        """
        Sends a GET request to the KVK basisprofiel API and returns the response.

        Args:
        -----------
        kvk_number (str): The KVK number of the company.
        geo_data (str): If True, returns geo data for the company.
        """
        if basis_profile_type:
            path = f"{APIpaths.basisprofielen}/{kvk_number}/{basis_profile_type}"
        else:
            path = f"{APIpaths.basisprofielen}/{kvk_number}"

        response = await self.__send_request("GET", path, geoData=geo_data)
        return response


    async def get_vestigingsprofiel(self, vestigingsnummer: str) -> aiohttp.ClientResponse:
        """
        Sends a GET request to the KVK vestigingsprofiel API and returns the response.

        Args:
        -----------
        vestigingsnummer (str): The branch number of the company.
        """

        path = f"{APIpaths.vestigingsprofielen}/{vestigingsnummer}"
        response = await self.__send_request("GET", path)
        return response



    async def get_naamgevingen(self, kvk_number: str) -> aiohttp.ClientResponse:
        """
        Sends a GET request to the KVK naamgevingen API and returns the response.

        Args:
        -----------
        kvk_number (str): The KVK number of the company.
        """

        path = f"{APIpaths.naamgevingen}/{kvk_number}"
        response = await self.__send_request("GET", path)
        return response

    async def get_companies(self,
                            kvk_number: Optional[str] = None,
                            rsin: Optional[str] = None,
                            vestigingsnummer: Optional[str] = None,
                            handelsnaam: Optional[str] = None,
                            straatnaam: Optional[str] = None,
                            plaats: Optional[str] = None,
                            postcode: Optional[str] = None,
                            huisnummer: Optional[str] = None,
                            huisnummerToevoeging: Optional[str] = None,
                            type: Optional[str] = None,
                            InclusiefInactieveRegistraties: Optional[bool] = None,
                            pagina: Optional[int] = None,
                            aantal: Optional[int] = None,
                            ) -> aiohttp.ClientResponse:
        """
        Sends a GET request to the KVK companies search API and returns
        the response.

        Args:
        -----------
        kvk_number (str, optional): Dutch Chamber of Commerce number: consists of 8 digits.
        rsin (str, optional): Legal Persons and Partnerships Information Number.
        vestigingsnummer (str, optional): The establishment number of the company.
        handelsnaam (str, optional): The name under which a branch or legal entity trades.
        straatnaam (str, optional): The street name of the company's address.
        plaats (str, optional): The city of the company's address.
        postcode (str, optional): Can only be searched in combination with Huisnummer.
        huisnummer (str, optional): Can only be searched in combination with Postcode.
        huisnummerToevoeging (str, optional): Optional. Only in combination with huisnummer. Consists of 1 to 4 characters (letters, numbers, characters: -, +, space).
        InclusiefInactieveRegistraties (bool, optional): Whether to include inactive registrations in the search results.
        type (str, optional): Filter by type: main branch, branch, and/or legal entity.
        pagina (int, optional): Page number, at least 1 and at most 1000.
        aantal (int, optional): Choose the number of results per page, at least 1 and at most 100.

        Returns:
        -----------
        requests.Response: The HTTP response object containing the search results.

        Raises:
        -----------
        ValueError: If the required environment variables are not set.

        Example usage:
        -----------
            >>> kvk = KVK(test=True)
            >>> response = kvk.get_companies(handelsnaam='Acme Corp', plaats='Amsterdam')
            >>> results = response.json()['data']['items']
        """


        if (huisnummer or postcode) and (not huisnummer or not postcode):
            raise ValueError('Huisnummer and postcode must be set together')

        if huisnummerToevoeging and not huisnummer:
            raise ValueError('HuisnummerToevoeging must be set together with huisnummer')

        response = await self.__send_request("GET",
                                             APIpaths.zoeken,
                                             kvkNummer=kvk_number,
                                             rsin=rsin,
                                             vestigingsnummer=vestigingsnummer,
                                             handelsnaam=handelsnaam,
                                             straatnaam=straatnaam,
                                             plaats=plaats,
                                             postcode=postcode,
                                             huisnummer=huisnummer,
                                             huisnummerToevoeging=huisnummerToevoeging,
                                             type=type,
                                             InclusiefInactieveRegistraties=InclusiefInactieveRegistraties,
                                             pagina=pagina,
                                             antal=aantal)
        return response
