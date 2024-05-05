import re
import encryption
import key_storage
import database
import queries
import wallet

def setup_account(alias):
    account = wallet.get_wallet().create_account()
    account.set_alias(alias=alias)
    return account

def store_keys(public_key, private_key, fernet_key, insurance_id):
    key_storage.store_keys(public_key, private_key, insurance_id)
    key_storage.store_fernet_key(fernet_key, insurance_id)

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

def insurance_id_validation(insurance_id):
    conn, cursor = database.connect()
    count = database.select(cursor, queries.get_insurance_id(insurance_id))
    database.close_connection(conn, cursor)
    return count[0][0]

def insurance_id_format_validation(insurance_id):
    pattern = re.compile(r'^[^DFIQUV]{2}\d{6}[A-Z]$')
    return bool(pattern.match(insurance_id))

def create_client(name, surname, insurance_id, password, is_doctor):
    if not password_validation(password):
        return 'Invalid password format'
    if not insurance_id_format_validation(insurance_id):
        return 'Invalid insurance ID format'
    
    # for doctors add a character to insurance_id
    if is_doctor is True:
        insurance_id = 'D' + insurance_id

    if insurance_id_validation(insurance_id) > 0:
        return 'Client with given insurance ID already exists in the system'
    
    # setup client account
    account = setup_account('active')
    account_id = account.get_metadata().index

    # generate fernet key and encrypt password
    fernet_key = encryption.generate_key()
    encrypted_password = encryption.encrypt_password(password, fernet_key)
    key_storage.store_fernet_key(fernet_key, account_id)

    # for patients generate and store paillier keys
    if is_doctor is False:
        public_key, private_key = encryption.generate_key_pair()
        key_storage.store_keys(public_key, private_key, account_id)

    # connect to database and insert new client
    conn, cursor = database.connect()
    database.update(cursor, queries.insert_client(name, surname, insurance_id, encrypted_password, is_doctor, account_id))

    # close database connection
    database.close_connection(conn, cursor)
    return 'Client creation was successfull'
    
if __name__ == "__main__":
    print(create_client('Anna', 'Taylor', 'AA987654G', 'Password23!', False))