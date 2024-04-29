import os
import json
import encryption
import key_storage
from dotenv import load_dotenv
from iota_sdk import utf8_to_hex, SendParams, TransactionOptions, TaggedDataPayload

load_dotenv()
node_url = os.getenv("NODE_URL")
exp_url = os.getenv("EXPLORER_URL")

def post_med_record(doctor_account, patient_account, tag, med_record):
    patient_address = get_address(patient_account)
    params = [SendParams(
        address=patient_address,
        amount=0,
    )]

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

# TEST
def test():
    import wallet

    w = wallet.get_wallet()
    doctor = w.get_account(0)
    patient = w.get_account(1)

    example_record = {
    "age": 18
    }
    post_med_record(doctor, patient, "Test record", example_record)

if __name__ == "__main__":
    test()
