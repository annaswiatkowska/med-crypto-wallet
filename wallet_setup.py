import os
from dotenv import load_dotenv
from iota_sdk import (ClientOptions, CoinType, StrongholdSecretManager, Utils, Wallet)

load_dotenv()

# node to connect to
node_url = os.getenv("NODE_URL")

# password to encrypt the stored data
STRONGHOLD_PASSWORD = os.getenv("STRONGHOLD_PASSWORD")

# path to store the account snapshot
STRONGHOLD_SNAPSHOT_PATH = 'vault.stronghold'

# Setup Stronghold secret manager
secret_manager = StrongholdSecretManager(
    STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)

# set up the wallet
client_options = ClientOptions(nodes=[node_url])

wallet = Wallet(
    client_options=client_options,
    coin_type=CoinType.SHIMMER,
    secret_manager=secret_manager
)

# generate a mnemonic and store its seed in the stronghold vault
mnemonic = Utils.generate_mnemonic()
print(f'Mnemonic: {mnemonic}')
wallet.store_mnemonic(mnemonic)
