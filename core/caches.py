""" This file contains all the different caches that may be used during execution
    TODO: Implement system for intelligently accessing and managing caches
"""

# Stores authenticated versions of any API that needs to be called in multiple different contexts
api_cache = {}

api_keys = {}

user_rules = {}

general_config = {}

provider_cache = {'home screen': None}
