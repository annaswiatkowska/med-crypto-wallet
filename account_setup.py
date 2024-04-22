# add check on executed queries
# TEST TEST TEST

import re
import encryption
import key_storage
import database
import queries
import wallet_setup

def setup_account():
    account = wallet_setup.get_wallet().create_account()
    return account, account.generate_ed25519_addresses(1)

def store_keys(public_key, private_key, fernet_key, user_id):
    key_storage.store_keys(public_key, private_key, user_id)
    key_storage.store_fernet_key(fernet_key, user_id)

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
    
    public_key, private_key = encryption.generate_key_pair()
    fernet_key = encryption.generate_key()
    encrypted_password = encryption.encrypt_value(password, fernet_key)
    account, address = setup_account()
    wallet_address = address[0].address

    # connect to database and insert new client
    conn, cursor = database.connect()
    database.insert(cursor, queries.insert_client(name, surname, insurance_id, encrypted_password, wallet_address, is_doctor))

    # update account alias and store keys
    query_result = database.select(cursor, queries.get_user_id(insurance_id))
    user_id = query_result[0][0]
    account.set_alias(str(user_id))
    store_keys(public_key, private_key, fernet_key, str(user_id))

    database.close_connection(conn, cursor)
    return 'Client creation was successfull'
    
if __name__ == "__main__":
    output = create_client('Alice', 'Smith', 'GG123456C', 'Password1!', False)
    print(output)