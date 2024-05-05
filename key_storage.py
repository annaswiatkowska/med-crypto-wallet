import json
import keyring
from phe import paillier

def store_keys(public_key, private_key, id):
    keyring.set_password('public_key', str(id), serialize_public_key(public_key))
    keyring.set_password('private_key', str(id), serialize_private_key(private_key))

def store_fernet_key(fernet_key, id):
    keyring.set_password('fernet_key', str(id), fernet_key.decode())

def get_both_keys(id):
    public_key = get_public_key(id)
    private_key = keyring.get_password('private_key', str(id))

    if public_key is None or private_key is None:
        return None, None
    return public_key, load_private_key(private_key, public_key)

def get_public_key(id):
    public_key = keyring.get_password('public_key', str(id))

    if public_key is None:
        return None
    return load_public_key(public_key)

def get_fernet_key(id):
    fernet_key = keyring.get_password('fernet_key', str(id))

    if fernet_key is None:
        return None
    return fernet_key.encode()

def remove_key(id, key_type):
    keyring.delete_password(key_type, str(id))

def serialize_public_key(public_key):
    dict = {}
    dict['public_key'] = {'n': public_key.n}
    return json.dumps(dict)

def serialize_private_key(private_key):
    dict = {}
    dict['private_key'] = {'p': private_key.p,
                           'q': private_key.q}
    return json.dumps(dict)

def load_public_key(serialised_public_key):
    dict = json.loads(serialised_public_key)
    pk = dict['public_key']
    return paillier.PaillierPublicKey(n=int(pk['n']))

def load_private_key(serialised_private_key, public_key):
    dict = json.loads(serialised_private_key)
    pk = dict['private_key']
    return paillier.PaillierPrivateKey(public_key,
                                       p=int(pk['p']),
                                       q=int(pk['q']))

# TEST
def test():
    public_key, private_key = paillier.generate_paillier_keypair()
    value = 133
    encrypted_value = public_key.encrypt(value)

    store_keys(public_key, private_key, 'test1')
    pub_key, priv_key = get_both_keys('test1')
    
    decrypted_value = priv_key.decrypt(encrypted_value)
    print(decrypted_value)

if __name__ == "__main__":
    test()
