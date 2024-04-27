import os
from dotenv import load_dotenv
import json
from dataclasses import asdict
from iota_sdk import SendParams, Client, TransactionOptions, hex_to_utf8, utf8_to_hex, OutputParams, Account, List

import wallet
import encryption
from phe import paillier

load_dotenv()
node_url = os.getenv("NODE_URL")
exp_url = os.getenv("EXPLORER_URL")

def send_transaction(account):
    client_address = get_address(account)
    account.sync()

    params = List(client_address, '0')

    transaction = account.send_transaction(params, TransactionOptions(allow_micro_amount=True))
    print(f'Block sent: {exp_url}/block/{transaction.blockId}')

def post_block(info):
    client = Client(nodes=[node_url])

    # Create and post a block with a tagged data payload
    block = client.build_and_post_block(
        tag=utf8_to_hex("Test"), data=utf8_to_hex(info), secret_manager=wallet.get_secret_manager(), account_index=0)

    print(f'Data block sent: {os.environ["EXPLORER_URL"]}/block/{block[0]}')

    block = client.get_block_data(block[0])
    print(f'Block data: {json.dumps(asdict(block), indent=4)}')

    payload = block.payload
    print(payload)
    data = hex_to_utf8(payload.data)
    return data
    

def get_address(account):
    return account.addresses()[0].address

# TEST
def test1():
    example_data = {
    "name": "John",
    "age": 30
    }

    pub, priv = encryption.generate_key_pair()
    enc = encryption.encrypt_dict(pub, example_data)

    out = post_block(json.dumps(enc))
    dict = json.loads(out)
    dec = encryption.decrypt_dict(pub, priv, dict)
    print(dec)

def test2():
    data = 11
    pub, priv = encryption.generate_key_pair()
    enc = encryption.encrypt_data(pub, data)

    out = post_block(str(enc))
    dec = encryption.decrypt_data(pub, priv, int(out))
    print(dec)

if __name__ == "__main__":
    w = wallet.get_wallet()
    acc = w.get_account(0)
    send_transaction(acc)
