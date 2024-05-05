import json
import keyring
from phe import paillier

# store keys in the keyring under client's account id
def store_keys(public_key, private_key, id):
    keyring.set_password("public_key", str(id), serialise_public_key(public_key))
    keyring.set_password("private_key", str(id), serialise_private_key(private_key))

def store_fernet_key(fernet_key, id):
    keyring.set_password("fernet_key", str(id), fernet_key.decode())

# retrieve paillier keys from keyring before conversion
def get_both_keys(id):
    public_key = get_public_key(id)
    private_key = keyring.get_password("private_key", str(id))

    if public_key is None or private_key is None:
        return None, None
    return public_key, load_private_key(private_key, public_key)

def get_public_key(id):
    public_key = keyring.get_password("public_key", str(id))

    if public_key is None:
        return None
    return load_public_key(public_key)

# retrieve fernet key from keyring
def get_fernet_key(id):
    fernet_key = keyring.get_password("fernet_key", str(id))

    if fernet_key is None:
        return None
    return fernet_key.encode()

# remove any key type from keyring for given user's account id
def remove_key(id, key_type):
    keyring.delete_password(key_type, str(id))

# serialise paillier keys before storing
def serialise_public_key(public_key):
    dict = {}
    dict["public_key"] = {"n": public_key.n}
    return json.dumps(dict)

def serialise_private_key(private_key):
    dict = {}
    dict["private_key"] = {"p": private_key.p,
                           "q": private_key.q}
    return json.dumps(dict)

# convert retrieved paillier keys back to proper type
def load_public_key(serialised_public_key):
    dict = json.loads(serialised_public_key)
    pk = dict["public_key"]
    return paillier.PaillierPublicKey(n=int(pk["n"]))

def load_private_key(serialised_private_key, public_key):
    dict = json.loads(serialised_private_key)
    pk = dict["private_key"]
    return paillier.PaillierPrivateKey(public_key,
                                       p=int(pk["p"]),
                                       q=int(pk["q"]))
