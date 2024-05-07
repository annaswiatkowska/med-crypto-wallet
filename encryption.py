from phe import paillier
from cryptography.fernet import Fernet

# Paillier keys functions
def generate_key_pair():
    return paillier.generate_paillier_keypair()

def to_numerical(string):
    # define mapping for non-numerical data and convert to numerical form
    string_mapping = {char: ord(char) for char in string}
    return [string_mapping[char] for char in string]

def to_string(num_list):
    # convert list of numbers back to string
    return ''.join([chr(num) for num in num_list])

# encrypt medical record
def encrypt_num(public_key, num):
    num = int(num * 1000)
    enc = public_key.encrypt(num)
    return enc.ciphertext()

def encrypt_letter(public_key, letter):
    enc = public_key.encrypt(letter)
    return enc.ciphertext()

def encrypt_list(public_key, list):
   return [encrypt_letter(public_key, num) for num in list]

def encrypt_dict(public_key, dict):
    for key in dict:
        data = dict[key]
        if isinstance(data, int) or isinstance(data, float):
            out = encrypt_num(public_key, dict[key])
        else:
            num = to_numerical(data)
            out = encrypt_list(public_key, num)
        dict[key] = out
    return dict

# decrypt medical record
def decrypt_num(public_key, private_key, num):
    enc_num = paillier.EncryptedNumber(public_key, num)
    dec_num = private_key.decrypt(enc_num)
    float_num = float(dec_num/1000)
    if float_num.is_integer():
        return int(float_num)
    return float_num

def decrypt_letter(public_key, private_key, letter):
    enc_letter = paillier.EncryptedNumber(public_key, letter)
    return private_key.decrypt(enc_letter)

def decrypt_list(public_key, private_key, list):
    return [decrypt_letter(public_key, private_key, num) for num in list]

def decrypt_dict(public_key, private_key, dict):
    for key in dict:
        data = dict[key]
        if isinstance(data, list):
            out = to_string(decrypt_list(public_key, private_key, data))
        else:
            out = decrypt_num(public_key, private_key, data)
        dict[key] = out
    return dict

# Fernet key functions
def generate_key():
    return Fernet.generate_key()

def encrypt_password(value, key):
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()

def decrypt_password(encrypted_value, key):
    f = Fernet(key)
    return f.decrypt(encrypted_value.encode()).decode()
