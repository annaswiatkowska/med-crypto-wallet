def insert_client(name, surname, insurance_id, password, wallet_address, is_doctor, wallet_id):
    return f"INSERT INTO users (name, surname, insurance_id, password, wallet_address, is_doctor, wallet_id) VALUES ('{name}', '{surname}', '{insurance_id}', '{password}', '{wallet_address}', {is_doctor}, {wallet_id});"

def get_user_id(insurance_id):
    return f"SELECT user_id FROM users WHERE insurance_id = '{insurance_id}';"