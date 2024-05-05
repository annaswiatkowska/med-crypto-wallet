import wallet
import queries
import database
import encryption
import key_storage

def validate_credentials(insurance_id, password):
    account_id = retrieve_account_id(insurance_id)

    conn, cursor = database.connect()
    enc_password = database.select(cursor, queries.get_encrypted_password(insurance_id))[0][0]
    database.close_connection(conn, cursor)

    key = key_storage.get_fernet_key(account_id)
    dec_password = encryption.decrypt_password(enc_password, key)
    if password == dec_password:
        return wallet.get_wallet().get_account(account_id)
    return 'Password and/or Insurance ID are invalid'

def retrieve_account_id(insurance_id):
    conn, cursor = database.connect()
    try:
        account_id = database.select(cursor, queries.get_account_id(insurance_id))[0][0]
    except:
        database.close_connection(conn, cursor)
        return 'Account ID not found for given Insurance ID'
    database.close_connection(conn, cursor)
    return account_id

def delete_account(insurance_id):
    if insurance_id.startswith('D'):
        return 'Deleting doctor account is not permitted'
    
    # retrieve corresponding account and mark it as deactivated
    account_id = retrieve_account_id(insurance_id)
    account = wallet.get_wallet().get_account(account_id)
    account.set_alias('deactivated')

    # retrieve account ID and remove all corresponding encryption keys
    account_id = account.get_metadata().index
    remove_all_keys(account_id)

    # delete account record from local database
    conn, cursor = database.connect()
    account_id = database.update(cursor, queries.remove_client_record(insurance_id))
    database.close_connection(conn, cursor)

    return 'Account was deleted successfully'


def remove_all_keys(account_id):
    key_storage.remove_key(account_id, 'public_key')
    key_storage.remove_key(account_id, 'private_key')
    key_storage.remove_key(account_id, 'fernet_key')

# TEST
if __name__ == "__main__":
    print(delete_account('AA987654G'))