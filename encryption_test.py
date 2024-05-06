import unittest
from encryption import *

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.public_key, self.private_key = generate_key_pair()
        self.fernet_key = generate_key()

    # test simple encryption and decryption of a number
    def test_paillier_encryption_decryption(self):
        num = 123
        encrypted_num = encrypt_num(self.public_key, num)
        decrypted_num = decrypt_num(self.public_key, self.private_key, encrypted_num)
        self.assertEqual(num, decrypted_num)

    # test password encryption and decryption via fernet key
    def test_fernet_encryption_decryption(self):
        password = "password123"
        encrypted_password = encrypt_password(password, self.fernet_key)
        decrypted_password = decrypt_password(encrypted_password, self.fernet_key)
        self.assertEqual(password, decrypted_password)

    # test encryption and decyption of a dict via pailliers keys
    def test_paillier_encryption_dict(self):
        data_dict = {'age': 25, 'name': 'Alice', 'height': 175.5}
        encrypted_dict = encrypt_dict(self.public_key, data_dict)
        decrypted_dict = decrypt_dict(self.public_key, self.private_key, encrypted_dict)
        self.assertDictEqual(data_dict, decrypted_dict)

if __name__ == '__main__':
    unittest.main()
