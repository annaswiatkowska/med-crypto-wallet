import re
import account
import encryption
import key_storage
import database
import queries
import wallet

def setup_account(alias, is_doctor):
    account = wallet.wallet.create_account()
    account.set_alias(alias=alias)
    # for doctors request test funds
    if is_doctor is True:
        address = account.addresses()[0].address
        wallet.request_funds(address)
    return account

def password_validation(password):
    if len(password) < 8:  
        return False
    if not re.search("[a-z]", password):  
        return False
    if not re.search("[A-Z]", password):  
        return False
    if not re.search("[0-9]", password):  
        return False
    if not re.search(r"[!@#$%^&*()-_=+{};:,<.>/?\|`~]", password):
        return False
    return True

def insurance_id_validation(insurance_id, cursor):
    return database.select(cursor, queries.get_insurance_id(insurance_id))

def insurance_id_format_validation(insurance_id):
    pattern = re.compile(r"^[^DFIQUV]{2}\d{6}[A-Z]$")
    return bool(pattern.match(insurance_id))

def create_client(name, surname, insurance_id, password, is_doctor, cursor):
    # check formatting for inputted password and insurance number
    if not password_validation(password):
        print("Invalid password format")
        return False
    if not insurance_id_format_validation(insurance_id):
        print("Invalid insurance ID format")
        return False
    
    # for doctors add a character to insurance_id
    if is_doctor is True:
        insurance_id = "D" + insurance_id

    # check if user with that id already exists in local database
    if insurance_id_validation(insurance_id, cursor) > 0:
        print("Client with given insurance ID already exists in the system")
        return False
    
    # setup client account and set it as active
    acc = setup_account("active", is_doctor)
    acc_id = acc.get_metadata().index

    # generate fernet key and encrypt password
    fernet_key = encryption.generate_key()
    encrypted_password = encryption.encrypt_password(password, fernet_key)
    key_storage.store_fernet_key(fernet_key, acc_id)

    # for patients generate and store paillier keys
    if is_doctor is False:
        public_key, private_key = encryption.generate_key_pair()
        key_storage.store_keys(public_key, private_key, acc_id)

    # insert new client into local database
    try:
        database.update(cursor, queries.insert_client(name, surname, insurance_id, encrypted_password, is_doctor, acc_id))
    except Exception as e:
        print("Error message on client insertion to database: ", e)
        # if insertion was unsuccessful deactivated generated account and remove stored keys before retrying
        acc.set_alias("deactivated")
        account.remove_all_keys(acc_id)
        return False

    print("Client creation was successfull")
    return True
