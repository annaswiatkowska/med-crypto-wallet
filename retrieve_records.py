import json
import wallet
import encryption
import key_storage
from iota_sdk import SyncOptions, hex_to_utf8

def retrieve_records_list(patient_account):
    addresses = [acc.addresses()[0].address]
    opt = SyncOptions(addresses=addresses, force_syncing=True, sync_incoming_transactions=True)
    acc.set_default_sync_options(options=opt)
    acc.sync()

    raw_list = patient_account.incoming_transactions()
    filtered_list = []

    for transaction in raw_list:
        obj = json.dumps(transaction.payload, indent=4)
        dict = json.loads(obj)
        if 'essence' in dict:
            essence = dict['essence']
            if 'payload' in essence:
                payload = essence['payload']
                if 'tag' in payload and 'data' in payload:
                    tag = payload['tag']
                    data = payload['data']
                    filtered_list.append([hex_to_utf8(tag), hex_to_utf8(data)])
    
    return filtered_list

def decrypt_record(patient_account, record):
    tag = record[0]
    data = record[1]

    encrypted_data = json.loads(data)
    public_key, private_key = key_storage.get_both_keys(patient_account.get_metadata().alias)
    decrytpted_data = encryption.decrypt_dict(public_key, private_key, encrypted_data)
    return [tag, decrytpted_data]

if __name__ == "__main__":
    w = wallet.get_wallet()
    acc = w.get_account(3)
    record_list = retrieve_records_list(acc)
    print(decrypt_record(acc, record_list[0]))