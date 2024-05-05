def insert_client(name, surname, insurance_id, password, is_doctor, account_id):
    return f"INSERT INTO users (name, surname, insurance_id, password, is_doctor, account_id) VALUES ('{name}', '{surname}', '{insurance_id}', '{password}', {is_doctor}, {account_id});"

def get_encrypted_password(insurance_id):
    return f"SELECT password FROM users WHERE insurance_id = '{insurance_id}';"

def get_account_id(insurance_id):
    return f"SELECT account_id FROM users WHERE insurance_id = '{insurance_id}';"

def get_is_doctor(account_id):
    return f"SELECT is_doctor FROM users WHERE account_id = {account_id};"

def get_insurance_id(insurance_id):
    return f"SELECT COUNT(*) FROM users WHERE insurance_id = '{insurance_id}';"

def remove_client_record(insurance_id):
    return f"DELETE FROM users WHERE insurance_id = '{insurance_id}';"