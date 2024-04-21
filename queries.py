def insert_client(name, surname, insurance_id, password, wallet_address, is_doctor):
    return f'INSERT INTO users (name, surname, insurance_id, password, wallet_address, is_doctor) VALUES ({name}, {surname}, {insurance_id}, {password}, {wallet_address}, {is_doctor})'

def get_number_of_clients():
    return 'SELECT COUNT(*) FROM users;'