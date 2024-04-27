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

def encrypt_data(public_key, data):
    enc = public_key.encrypt(data)
    return enc.ciphertext()

def encrypt_list(public_key, list):
   return [encrypt_data(public_key, num) for num in list]

def encrypt_dict(public_key, dict):
    for key in dict:
        data = dict[key]
        if isinstance(data, int) or isinstance(data, float):
            out = encrypt_data(public_key, dict[key])
        elif isinstance(data, bool):
            out = encrypt_data(public_key, int(dict[key]))
        else:
            num = to_numerical(data)
            out = encrypt_list(public_key, num)
        dict[key] = out
    return dict

def decrypt_data(public_key, private_key, data):
    enc_num = paillier.EncryptedNumber(public_key, data)
    return private_key.decrypt(enc_num)

def decrypt_list(public_key, private_key, list):
    return [decrypt_data(public_key, private_key, num) for num in list]

def decrypt_dict(public_key, private_key, dict):
    for key in dict:
        data = dict[key]
        if isinstance(data, list):
            out = to_string(decrypt_list(public_key, private_key, data))
        else:
            out = decrypt_data(public_key, private_key, data)
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

# TEST 1
def test1():
    example_data = {
    "name": "John Doe",
    "age": 30,
    "height": 175.5,
    "student": True
    }

    pub, priv = generate_key_pair()
    encrypt_dict(pub, example_data)
    print(example_data)

    decrypt_dict(priv, example_data)
    print(example_data)

# TEST 2
def test2():
    fernet_key = generate_key()
    value = 'password123'
    encrypted_value = encrypt_password(value, fernet_key)
    print("Encrypted value:", encrypted_value)

    decrypted_value = decrypt_password(encrypted_value, fernet_key)
    print("Decrypted value:", decrypted_value)

if __name__ == "__main__":
    test1()
