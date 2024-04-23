import os
from dotenv import load_dotenv
from iota_sdk import Client

load_dotenv()
node_url = os.getenv("NODE_URL")

client = Client(nodes=[node_url])

node_info = client.get_info()
print(f'{node_info}')