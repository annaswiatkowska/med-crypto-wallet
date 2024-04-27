import os
from dotenv import load_dotenv
import json
from dataclasses import asdict
from iota_sdk import hex_to_utf8, utf8_to_hex, AddressAndAmount, SendParams, TransactionOptions, TaggedDataPayload

import wallet
import encryption
from phe import paillier

load_dotenv()
node_url = os.getenv("NODE_URL")
exp_url = os.getenv("EXPLORER_URL")

def post_block(info):
    client = wallet.get_wallet().get_client()

    add = AddressAndAmount(142600, 'rms1qpmw64ffph9utmydcd9ehwpyuk20g34lqtfxem547y6hwc9sd8qrwq378xy')

    block = client.build_and_post_block(
        tag=utf8_to_hex("Test"), 
        data=utf8_to_hex(info), 
        secret_manager=wallet.get_secret_manager(), 
        account_index=0, 
        initial_address_index=0,
        output=add
    )

    print(f'Data block sent: {os.environ["EXPLORER_URL"]}/block/{block[0]}')

    block = client.get_block_data(block[0])
    print(f'Block data: {json.dumps(asdict(block), indent=4)}')

    payload = block.payload
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
    acc = wallet.get_wallet().get_account(1)

    params = [SendParams(
        address="rms1qpm4gar4tv8drq3u5gzp4pfwam9ggrsklc4gf9xts2qsp96hxn9avs9sh5x",
        amount=0,
    )]

    taggedData = TaggedDataPayload(tag=utf8_to_hex("Test"), data=utf8_to_hex("Example"))
    options = TransactionOptions(allow_micro_amount=True, tagged_data_payload=taggedData)

    transaction = acc.send_with_params(params, options)
    print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{transaction.blockId}')
