import os
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()

try:
  server_env = os.getenv("SERVER_ENV")
  if not server_env:
    raise KeyError('environment variable SERVER_ENV not set.')

  if server_env == "production":
    from .production_settings import *
  elif server_env == "development":
    from .development_settings import *
  else:
    raise KeyError('invalid server environment.')

except KeyError as error:
  raise ImproperlyConfigured(error)
