import os
from dotenv import load_dotenv
from iota_sdk import (ClientOptions, CoinType, StrongholdSecretManager, Utils, Wallet)

load_dotenv()
node_url = os.getenv("NODE_URL")
snapshot_path = os.getenv("STRONGHOLD_SNAPSHOT_PATH")
stronghold_password = os.getenv("STRONGHOLD_PASSWORD")

def get_secret_manager():
    return StrongholdSecretManager(snapshot_path, stronghold_password)

# retrieve wallet instance
def get_wallet():
    secret_manager = get_secret_manager()
    client_options = ClientOptions(nodes=[node_url])
    wallet = Wallet(
        client_options=client_options,
        coin_type=CoinType.SHIMMER,
        secret_manager=secret_manager
    )
    return wallet

# global wallet instance
wallet = get_wallet()

# request test funds from IOTA
def request_funds(address):
    url = os.environ.get("FAUCET_URL")
    resp = wallet.get_client().request_funds_from_faucet(url, address)
    return resp
