import wallet
import queries
import database
import encryption
import key_storage

def validate_credentials(insurance_id, password, cursor):
    # try retrieving account id
    account_id = database.select(cursor, queries.get_account_id(insurance_id))
    if account_id is None:
        print("No account ID found for given insurance number")
        return None
    
    # try retrieving encrypted password for given account id
    enc_password = database.select(cursor, queries.get_encrypted_password(account_id))
    if enc_password is None:
        print("No password found for given account ID")
        return None

    # retrieve fernet key by account id and validate password
    key = key_storage.get_fernet_key(account_id)
    dec_password = encryption.decrypt_password(enc_password, key)
    if password == dec_password:
        return wallet.wallet.get_account(account_id)
    
    print("Password and/or Insurance ID are invalid")
    return None

# not added to main
def delete_account(insurance_id, cursor):
    if insurance_id.startswith("D"):
        return "Deleting doctor account is not permitted"
    
    # retrieve corresponding account and mark it as deactivated
    account_id = database.select(cursor, queries.get_account_id(insurance_id))
    account = wallet.wallet.get_account(account_id)
    account.set_alias("deactivated")

    # retrieve account ID and remove all corresponding encryption keys
    account_id = account.get_metadata().index
    remove_all_keys(account_id)

    # delete account record from local database
    account_id = database.update(cursor, queries.remove_client_record(insurance_id))
    return "Account was deleted successfully"

def remove_all_keys(account_id):
    key_storage.remove_key(account_id, "public_key")
    key_storage.remove_key(account_id, "private_key")
    key_storage.remove_key(account_id, "fernet_key")
