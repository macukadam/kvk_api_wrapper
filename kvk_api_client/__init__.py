import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
load_dotenv()

from .sync_client import KVK
from .async_client import KVK as AsyncKVK
