import os
from dotenv import load_dotenv

load_dotenv() 

database = os.environ.get('database', 'Store')
database_config = {'user': os.environ.get('user'), 'password': os.environ.get('password'), 'host': os.environ.get('host')}

print(database_config)