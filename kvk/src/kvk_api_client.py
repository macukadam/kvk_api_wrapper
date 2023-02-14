"""A very simple wrapper around KVK api."""

import warnings
from enum import Enum
import os
import requests
from dotenv import load_dotenv

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
load_dotenv()


class APIpaths(Enum):
    """API paths for KVK api."""

    # With the Basisprofiel API you can request extensive information from companies from the Trade Register
    basisprofielen = 'basisprofielen'
    # With the Zoeken API you can look up companies in the Trade Register. You can then request the data using another API.
    zoeken = 'zoeken'
    # With the Vestigingsprofiel API you request specific information from companies from the Trade Register.
    vestigingsprofielen = 'vestigingsprofielen'
    # With the Naamgeving API you request name data of companies from the Trade Register.
    naamgevingen = 'naamgevingen/kvknummer'


class BasisProfielPaths(Enum):
    """Basic profile paths for KVK api."""

    # Retrieve owner information for a specific company.
    eigenaar = 'eigenaar'
    # Retrieve head office information for a specific company.
    hoodfvestiging = 'hoofdvestiging'
    # Retrieve a list of branches for a specific company.
    vestigingen = 'vestigingen'


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
        >>> response = kvk.get_basis_profiel('12345678')
    """

    def __init__(self, test: bool) -> None:

        self.host = os.getenv('KVK_HOST')
        self.api_version = os.getenv('KVK_API_VERSION')
        self.api_key = os.getenv('KVK_APIKEY_PROD')
        self.api_version = os.getenv('KVK_API_VERSION')

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

    def __send_request(self, request_type, *res, **params) \
            -> requests.Response:

        if self.host is None:
            raise ValueError('HOST is not set')

        url = self.host + ''.join(['/' + r for r in (self.api_version, *res)
                                   if r is not None])

        response = requests.request(
            request_type, url, headers=self.headers, params=params,
            verify=False)

        return response

    def get_basis_profiel(self, kvk_number: str,
                          basis_profile_type: BasisProfielPaths | None = None,
                          geo_data: str = "False") -> requests.Response:
        """
        Sends a GET request to the KVK basisprofiel API and returns the response.

        Args:
        -----------
        kvk_number (str): The KVK number of the company.
        geo_data (str): If True, returns geo data for the company.
        """
        if basis_profile_type:
            basis_profile_type = basis_profile_type.value

        response = self.__send_request("GET",
                                       APIpaths.basisprofielen.value,
                                       kvk_number,
                                       basis_profile_type,
                                       geoData=geo_data)

        return response

    def get_vestigingsprofiel(self, vestigingsnummer: str) -> requests.Response:
        """
        Sends a GET request to the KVK vestigingsprofiel API and returns the response.

        Args:
        -----------
        vestigingsnummer (str): The branch number of the company.
        """

        response = self.__send_request("GET",
                                       APIpaths.vestigingsprofielen.value,
                                       vestigingsnummer)

        return response

    def get_naamgevingen(self, kvk_number: str) -> requests.Response:
        """
        Sends a GET request to the KVK naamgevingen API and returns the response.

        Args:
        -----------
        kvk_number (str): The KVK number of the company.
        """

        response = self.__send_request("GET",
                                       APIpaths.naamgevingen.value,
                                       kvk_number)

        return response

    def get_companies(self,
                      kvk_number: str | None = None,
                      rsin: str | None = None,
                      vestigingsnummer: str | None = None,
                      handelsnaam: str | None = None,
                      straatnaam: str | None = None,
                      plaats: str | None = None,
                      postcode: str | None = None,
                      huisnummer: str | None = None,
                      huisnummerToevoeging: str | None = None,
                      type: str | None = None,
                      InclusiefInactieveRegistraties: bool | None = None,
                      pagina: int | None = None,
                      aantal: int | None = None,
                      ) -> requests.Response:
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
            raise ValueError(
                'Huisnummer and postcode must be set together')

        if huisnummerToevoeging and not huisnummer:
            raise ValueError(
                'HuisnummerToevoeging must be set together with huisnummer')

        response = self.__send_request("GET",
                                       APIpaths.zoeken.value,
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

