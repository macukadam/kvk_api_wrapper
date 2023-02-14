# KVK API Client

This is a Python client for the KVK API, which provides access to the Dutch Chamber of Commerce (KVK) company register.

## Installation

You can install the package into your project via pip:

```sh
pip install kvk_api_client
```

# USAGE

To use the KVK API client, you first need to set up environment variables for the required credentials:

```sh
export KVK_HOST='https://api.kvk.nl'
export KVK_API_VERSION='api/v1'
export KVK_APIKEY_TEST='your-test-api-key'
export KVK_APIKEY_PROD='your-production-api-key'
```

# EXAMPLE

By setting the test parameter to true, you can play arround with api:
https://developers.kvk.nl/documentation/testing

```python
from kvk_api_client import KVK

# Create a KVK API client instance
kvk = KVK(test=True)

# Call an API method
companies = kvk.get_companies(kvk_number="12312312")
```

# TESTS

Make sure pytest is installed on your environment

```sh
python3 -m pytest
```
