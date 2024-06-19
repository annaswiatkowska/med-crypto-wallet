def insert_client(name, surname, insurance_id, password, is_doctor, account_id):
    return f"INSERT INTO users (name, surname, insurance_id, password, is_doctor, account_id) VALUES ('{name}', '{surname}', '{insurance_id}', '{password}', {is_doctor}, {account_id});"

def remove_client_record(insurance_id):
    return f"DELETE FROM users WHERE insurance_id = '{insurance_id}';"

# password validation on login
def get_encrypted_password(account_id):
    return f"SELECT password FROM users WHERE account_id = '{account_id}';"

def get_account_id(insurance_id):
    return f"SELECT account_id FROM users WHERE insurance_id = '{insurance_id}';"

# doctor authorisation on sending records
def get_is_doctor(account_id):
    return f"SELECT is_doctor FROM users WHERE account_id = {account_id};"

# insurance_id validation
def get_insurance_id(insurance_id):
    return f"SELECT COUNT(*) FROM users WHERE insurance_id = '{insurance_id}';"

# check if permission exists
def get_permission(patient_acc_id, doctor_acc_id):
    return f"SELECT EXISTS(SELECT 1 from permissions where patient_acc_id = {patient_acc_id} and doctor_acc_id = {doctor_acc_id});"

def grant_permission(patient_acc_id, doctor_acc_id):
    return f"INSERT INTO permissions (patient_acc_id, doctor_acc_id) VALUES ({patient_acc_id}, {doctor_acc_id});"

def revoke_permission(patient_acc_id, doctor_acc_id):
    return f"DELETE FROM permissions WHERE patient_acc_id = {patient_acc_id} AND doctor_acc_id = {doctor_acc_id};"

def search_doctor(doctor_surname):
    return f"SELECT account_id, name, surname FROM users WHERE surname = '{doctor_surname}';"

def list_permissions(patient_acc_id):
    return f"SELECT account_id, name, surname from users u join permissions p on u.account_id = p.doctor_acc_id where p.patient_acc_id = {patient_acc_id};"