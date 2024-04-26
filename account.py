import wallet
import queries
import database
import encryption
import key_storage

def validate_credentials(insurance_id, password):
    key = key_storage.get_fernet_key(insurance_id)

    conn, cursor = database.connect()
    enc_password = database.select(cursor, queries.get_encrypted_password(insurance_id))[0][0]
    database.close_connection(conn, cursor)

    dec_password = encryption.decrypt_password(enc_password, key)
    if password == dec_password:
        return retrieve_account(insurance_id)
    return 'Password and/or Insurance ID are invalid'

def retrieve_account(insurance_id):
    conn, cursor = database.connect()
    account_id = database.select(cursor, queries.get_account_id(insurance_id))[0][0]
    database.close_connection(conn, cursor)
    return wallet.get_wallet().get_account(account_id)

# TEST
if __name__ == "__main__":
    print(validate_credentials('CC123456Y', 'Florida7!'))