# add check on insurance_id
# add check on executed queries
# TEST TEST TEST

import re
import encryption
import key_storage
import database
import queries
import wallet_setup

def setup_account(user_id):
    account = wallet_setup.get_wallet().create_account(user_id)
    return account.generate_ed25519_addresses(1)

def generate_and_store_keys(user_id):
    public_key, private_key = encryption.generate_key_pair
    fernet_key = encryption.generate_key()

    key_storage.store_keys(public_key, private_key, user_id)
    key_storage.store_fernet_key(user_id, fernet_key)

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

def create_client(name, surname, insurance_id, password, is_doctor):
    if not password_validation(password):
        return 'Invalid password'
    
    conn, cursor = database.connect()
    result = database.execute_query(cursor, queries.get_number_of_clients())
    user_id = result[0][0] + 1

    generate_and_store_keys()
    key = key_storage.get_fernet_key(user_id)
    encrypted_password = encryption.encrypt_value(password, key)

    wallet_address = setup_account(user_id)
    database.execute_query(cursor, queries.insert_client(name, surname, insurance_id, encrypted_password, wallet_address, is_doctor))

    database.close_connection(conn, cursor)
    
if __name__ == "__main__":
    output = create_client('Alice', 'Smith', 'QQ123456C', 'Password1!', False)
    print(output)