import atexit
import wallet
import account
import database
import queries
import post_record
import retrieve_records
import account_setup

connection, cursor = database.connect()

def close_database_connection():
    database.close_connection(connection, cursor)

# close database connection at script exit
atexit.register(close_database_connection)

def retrieve_patient(insurance_id):
    patient_acc_id = database.select(cursor, queries.get_account_id(insurance_id))
    if patient_acc_id is None:
        print("No account ID found for given insurance number, please retry")
        return None
    return wallet.wallet.get_account(int(patient_acc_id))

def doctor_view_choice(acc):
    while True:
        print("1. View patient's medical history")
        print("2. Post medical record")
        choice = input("Enter your choice number or press 'q' to exit: ")
        if choice == "1":
            while True:
                insurance_id = input("Enter patient's insurance number or press 'q' to go back to main view: ")
                if insurance_id == 'q':
                    break
                patient_account = retrieve_patient(insurance_id)
                if patient_account is None:
                    continue
                retrieve_user_records(patient_account)
        elif choice == "2":
            while True:
                insurance_id = input("Enter patient's insurance number or press 'q' to go back to main view: ")
                if insurance_id == 'q':
                    break
                patient_account = retrieve_patient(insurance_id)
                if patient_account is None:
                    continue
                prepare_and_post(acc, patient_account)
        elif choice == "q":
            break
        else:
            print("Invalid choice. Please try again or press 'q' to exit.")

def prepare_and_post(doctor_acc, patient_acc):
    title = input("Input title of medical record: ")
    print("Enter key-value pairs for the record (press 'Enter' without entering a key to stop):")
    record = {}
    max_count = 16
    while len(record) < max_count:
        key = input("Enter key: ")
        if not key:
            break  # Exit the loop if the user presses Enter without entering a key
        value = input("Enter value: ")
        
        # check if value is int or float
        try: 
            value = float(value)
        except: pass

        # If the value is a string, subtract its length from the maximum number of pairs
        if isinstance(value, str):
            max_pairs -= (len(value) - 1)

        record[key] = value

    print("Final Record:")
    print(record)
    post_record.post_med_record(doctor_acc, patient_acc, title, record, cursor)

def retrieve_user_records(acc):
    records_list = retrieve_records.retrieve_records_list(acc)

    # format list to show numbered record titles with timestamps
    visible_list = []
    record_number = 0
    for record in records_list:
        record_number = record_number + 1
        record_title =  str(record_number) + '. ' + str(record[0])
        visible_list.append(record_title)
    
    # print formatted list and prompt to choose which record to enter
    for item in visible_list:
        print(item)
    while True:
        num = input("Input the number of record you wish to read or press 'q' to exit: ")
        if num.isnumeric() and (int(num) < 0 or int(num) > record_number):
            print("Invalid record number, please try again.")
            continue
        elif num == 'q':
            break
        
        # adjust number to list indexing
        num = int(num) - 1
        dec_record = retrieve_records.decrypt_record(acc, records_list[num])
        for item in dec_record:
            print(item)

def proceed_after_login(acc):
    account_id = acc.get_metadata().index
    # check if given account belongs to a doctor
    is_doctor = database.select(cursor, queries.get_is_doctor(account_id))
    if is_doctor is True:
        doctor_view_choice(acc)
    else:
        # for patients enable only records view
        retrieve_user_records(acc)

def login():
    print("Login to your account: ")
    while True:
        insurance_id = input("Enter your insurance number: ")
        password = input("Enter your password: ")
        output = account.validate_credentials(insurance_id, password, cursor)
        if output is None:
            choice = input("Press 'q' if you wish to go back and register inestad: ")
            if choice == 'q':
                break
            continue
        else:
            acc = output
            print("Login is successful!")
            proceed_after_login(acc)

def register():
    print("Register your account: ")
    while True:
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        insurance_id = input("Enter your insurance number: ")
        password = input("Enter your password: ")

        # prompt to choose account type and repeat until given correct number
        while True:
            print("What account type you want to setup?")
            print("1. Patient")
            print("2. Doctor")
            is_doctor = input("Enter your choice: ")
            if is_doctor in ["1", "2"]:
                is_doctor = (is_doctor == "2")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

        output = account_setup.create_client(name, surname, insurance_id, password, is_doctor, cursor)
        if output is True:
            login()
            break
        else:
            choice = input("Press 'q' if you wish to go back and choose login option instead: ")
            if choice == 'q':
                break
            continue
        

def main():
    print("Welcome to the IOTA Medical Records Wallet!")
    # main "page" with options to register or login
    while True:
        print("1. Register")
        print("2. Login")
        choice = input("Enter your choice or press 'q' to exit: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "q":
            break
        else:
            print("Invalid choice. Please try again or press 'q' to exit.")


if __name__ == "__main__":
    main()