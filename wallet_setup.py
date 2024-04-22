import os
from dotenv import load_dotenv
from iota_sdk import (ClientOptions, CoinType, StrongholdSecretManager, Utils, Wallet)

load_dotenv()
node_url = os.getenv("NODE_URL")
snapshot_path = os.getenv("STRONGHOLD_SNAPSHOT_PATH")
stronghold_password = os.getenv("STRONGHOLD_PASSWORD")

def get_secret_manager():
    return StrongholdSecretManager(snapshot_path, stronghold_password)

def get_wallet():
    secret_manager = get_secret_manager()
    client_options = ClientOptions(nodes=[node_url])
    wallet = Wallet(
        client_options=client_options,
        coin_type=CoinType.SHIMMER,
        secret_manager=secret_manager
    )
    return wallet

# called once
def generate_mnemonic():
    mnemonic = Utils.generate_mnemonic()
    with open('mnemonic.txt', 'w') as file:
        file.write(mnemonic)
    get_wallet().store_mnemonic(mnemonic)

if __name__ == "__main__":
    wallet = get_wallet()
    wallet.remove_latest_account()
    print(wallet.get_accounts())