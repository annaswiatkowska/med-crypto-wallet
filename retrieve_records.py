import json
import wallet
import encryption
import key_storage
from iota_sdk import hex_to_utf8

import os
from dotenv import load_dotenv
from iota_sdk import Client
from dataclasses import asdict

def retrieve_records_list(patient_account):
    raw_list = patient_account.transactions()
    filtered_list = []

    for transaction in raw_list:
        blockId = transaction.blockId
        obj = json.dumps(transaction.payload, indent=4)
        dict = json.loads(obj)
        if 'essence' in dict:
            essence = dict['essence']
            if 'payload' in essence:
                payload = essence['payload']
                if 'tag' in payload and 'data' in payload:
                    tag = payload['tag']
                    filtered_list.append([hex_to_utf8(tag), blockId])
    
    return filtered_list

def retrieve_record(patient_account, record):
    load_dotenv()
    node_url = os.getenv("NODE_URL")
    client = Client(nodes=[node_url])
    block = client.get_block_data(record[1])

    tag = record[0]
    data = None
    obj = json.dumps(asdict(block.payload), indent=4)
    dict = json.loads(obj)
    if 'essence' in dict:
            essence = dict['essence']
            if 'payload' in essence:
                payload = essence['payload']
                if 'data' in payload:
                    data = hex_to_utf8(payload['data'])

    if data is not None:
        encrypted_data = json.loads(data)
        public_key, private_key = key_storage.get_both_keys(patient_account.get_metadata().alias)
        decrytpted_data = encryption.decrypt_dict(public_key, private_key, encrypted_data)
        return [tag, decrytpted_data]

if __name__ == "__main__":
    w = wallet.get_wallet()
    acc = w.get_account(1)
    records_list = retrieve_records_list(acc)
    print(retrieve_record(acc, records_list[0]))