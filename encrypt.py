from phe import paillier

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
    return public_key.encrypt(data)

def encrypt_list(public_key, list):
    return [public_key.encrypt(num) for num in list]

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

def decrypt_data(private_key, data):
    return private_key.decrypt(data)

def decrypt_list(private_key, list):
    return [private_key.decrypt(num) for num in list]

def decrypt_dict(private_key, dict):
    for key in dict:
        data = dict[key]
        if isinstance(data, list):
            out = to_string(decrypt_list(private_key, data))
        else:
            out = decrypt_data(private_key, data)
        dict[key] = out
    return dict

# example_data = {
#     "name": "John Doe",
#     "age": 30,
#     "height": 175.5,
#     "student": True
# }

# pub, priv = generate_key_pair()

# encrypt_dict(pub, example_data)
# print(example_data)

# decrypt_dict(priv, example_data)

# print(example_data)