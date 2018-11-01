# helpers for json and dict

from __future__ import print_function
from functools import reduce
import json

def jsonPrettyPrinter(parsedValue):
  print(json.dumps(parsedValue, indent=4, sort_keys=True))

def recursive_get(d, *keys):
  '''
    resolver for nested dicts
  '''
  return reduce(lambda c, k: c.get(k, {}), keys, d)