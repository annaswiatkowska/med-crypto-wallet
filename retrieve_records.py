import json
import encryption
import key_storage
from iota_sdk import SyncOptions, hex_to_utf8

# list all addresses associated with given account
def get_addresses(account):
    addresses = []
    for element in account.addresses():
        addresses.append(element.address)
    return addresses

def retrieve_records_list(patient_account):
    # sync patient's account for latest data
    addresses = get_addresses(patient_account)
    opt = SyncOptions(addresses=addresses, force_syncing=True, sync_incoming_transactions=True)
    patient_account.set_default_sync_options(options=opt)
    patient_account.sync()

    # retrieve all transactions received by the account
    raw_list = patient_account.incoming_transactions()

    # filter the list to save only valid transactions with tag and payload
    filtered_list = []
    for transaction in raw_list:
        obj = json.dumps(transaction.payload, indent=4)
        dict = json.loads(obj)
        if "essence" in dict:
            essence = dict["essence"]
            if "payload" in essence:
                payload = essence["payload"]
                if "tag" in payload and "data" in payload:
                    tag = payload["tag"]
                    data = payload["data"]
                    filtered_list.append([hex_to_utf8(tag), hex_to_utf8(data)])
                    
    return filtered_list

# decrypt and return data in chosen record
def decrypt_record(patient_account, record):
    tag = record[0]
    data = record[1]

    # message on invalid data format
    try:
        encrypted_data = json.loads(data)
    except:
        print("Data appears to be incorrectly formatted")

    # message in case data cannot be correctly decrypted by patient's key
    public_key, private_key = key_storage.get_both_keys(patient_account.get_metadata().index)
    try:
        decrytpted_data = encryption.decrypt_dict(public_key, private_key, encrypted_data)
    except:
        print("Data in record appears to be corrupted")
    return [tag, decrytpted_data]
