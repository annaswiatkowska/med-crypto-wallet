import re
import encryption
import key_storage
import database
import queries
import wallet

def setup_account(insurance_id):
    account = wallet.get_wallet().create_account(alias=insurance_id)
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
    pattern = re.compile(r'^[^DFIQUV]{2}\d{6}[A-Z]$')
    return bool(pattern.match(insurance_id))

def create_client(name, surname, insurance_id, password, is_doctor):
    if not password_validation(password):
        return 'Invalid password format'
    if not insurance_id_validation(insurance_id):
        return 'Invalid insurance ID format'
    
    # generate keys and encrypt password
    public_key, private_key = encryption.generate_key_pair()
    fernet_key = encryption.generate_key()
    store_keys(public_key, private_key, fernet_key, insurance_id)
    encrypted_password = encryption.encrypt_password(password, fernet_key)

    # setup client account
    account = setup_account(insurance_id)
    account_id = account.get_metadata().index

    # connect to database and insert new client
    conn, cursor = database.connect()
    database.insert(cursor, queries.insert_client(name, surname, insurance_id, encrypted_password, is_doctor, account_id))

    # close database connection
    database.close_connection(conn, cursor)
    return 'Client creation was successfull'
    
if __name__ == "__main__":
    output = create_client('Lily', 'Stone', 'BB654321Y', 'StarryNight9@!', True)
    print(output)