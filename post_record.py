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

def post_med_record(doctor_account, patient_account, title, med_record, cursor):
    # check doctor's account
    if doctor_authorisation(doctor_account, cursor) is False:
        print("Account attempting to send a record is not marked as doctor")
        return

    # check patient's account
    if doctor_authorisation(patient_account, cursor) is True:
        print('Posting records to account marked as doctor is not allowed')
        return
    
    # prepare addresses and parameters
    patient_address = patient_account.generate_ed25519_addresses(1)[0].address
    doctor_address = doctor_account.addresses()[0].address
    params = [SendParams(
        address=patient_address,
        amount=0,
        returnAddress=doctor_address,
        expiration=10
    )]

    # prepare tag and data and include in payload
    tag = get_tag(title)
    record = prepare_record(patient_account, med_record)
    taggedData = TaggedDataPayload(tag=utf8_to_hex(tag), data=utf8_to_hex(record))
    # allow microtransactions to send 0 funds
    options = TransactionOptions(allow_micro_amount=True, tagged_data_payload=taggedData)

    # attempt to send transaction with medical record
    try:
        transaction = doctor_account.send_with_params(params, options)
        print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{transaction.blockId}')
    except Exception as e:
        print("An exception occured: ", e)

# format medical record for transaction payload
def prepare_record(patient_account, record):
    id = patient_account.get_metadata().index
    public_key = key_storage.get_public_key(id)

    encrypted_record = encryption.encrypt_dict(public_key, record)
    return json.dumps(encrypted_record)

# return True if given doctor's account
def doctor_authorisation(account, cursor):
    is_doctor = database.select(cursor, queries.get_is_doctor(account.get_metadata().index))
    return is_doctor

# adds timestamp to tag
def get_tag(title):
    timestamp = datetime.datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return str(formatted_timestamp + ' ' + title)
