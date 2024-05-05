import os
import json
import queries
import database
import encryption
import key_storage
import datetime
from dotenv import load_dotenv
from iota_sdk import utf8_to_hex, SendParams, TransactionOptions, TaggedDataPayload

load_dotenv()
node_url = os.getenv("NODE_URL")
exp_url = os.getenv("EXPLORER_URL")

def post_med_record(doctor_account, patient_account, title, med_record):
    if doctor_authorisation(doctor_account) is False:
        print('Account attempting to send a record is not marked as doctor')
        return

    if doctor_authorisation(patient_account) is True:
        print('Posting records to account marked as doctor is not allowed')
        return
    
    patient_address = patient_account.generate_ed25519_addresses(1)[0].address
    doctor_address = get_address(doctor_account)
    params = [SendParams(
        address=patient_address,
        amount=0,
        returnAddress=doctor_address,
        expiration=10
    )]

    tag = get_tag(title)
    record = prepare_record(patient_account, med_record)
    taggedData = TaggedDataPayload(tag=utf8_to_hex(tag), data=utf8_to_hex(record))
    options = TransactionOptions(allow_micro_amount=True, tagged_data_payload=taggedData)

    try:
        transaction = doctor_account.send_with_params(params, options)
        print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{transaction.blockId}')
    except Exception as e:
        print('An exception occured: ', e)

def get_address(account):
    return account.addresses()[0].address

def prepare_record(patient_account, record):
    id = patient_account.get_metadata().alias
    public_key = key_storage.get_public_key(id)

    encrypted_record = encryption.encrypt_dict(public_key, record)
    return json.dumps(encrypted_record)

def doctor_authorisation(account):
    conn, cursor = database.connect()
    is_doctor = database.select(cursor, queries.get_is_doctor(account.get_metadata().index))[0][0]
    database.close_connection(conn, cursor)
    return is_doctor

def get_tag(title):
    timestamp = datetime.datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return str(formatted_timestamp + ' ' + title)

# TEST
def test():
    import wallet

    w = wallet.get_wallet()
    doctor = w.get_account(0)
    patient = w.get_account(1)

    example_record = {
    "age": 20,
    "height": 160,
    "something": 133,
    "other smth": 12.5,
    "some str": "AUTH",
    "someting else": 133.2,
    "others": "CMP",
    "example": 13,
    "example2": 122,
    "example3": 99,
    "example4": 100,
    "example5": 1
    }
    post_med_record(doctor, patient, "Max check", example_record)

if __name__ == "__main__":
    test()