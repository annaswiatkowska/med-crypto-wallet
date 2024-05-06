import unittest
from unittest.mock import patch, MagicMock
from account import validate_credentials

class TestAccountValidation(unittest.TestCase):
    
    @patch("account.database.select")
    @patch("account.key_storage.get_fernet_key")
    @patch("account.encryption.decrypt_password")
    def test_valid_credentials(self, mock_decrypt_password, mock_get_fernet_key, mock_select):
        # Mocking the database.select function to return expected values
        mock_select.side_effect = [1, "encrypted_password"]

        # Mocking key_storage.get_fernet_key
        mock_get_fernet_key.return_value = b'fernet_key'

        # Mocking encryption.decrypt_password
        mock_decrypt_password.return_value = "33LondonEye!"

        # Valid credentials
        result = validate_credentials("TT654321X", "33LondonEye!", MagicMock())

        # Assertions
        self.assertIsNotNone(result)
        self.assertTrue(str(result).startswith("<iota_sdk.wallet.account.Account object at"))

    @patch("account.database.select")
    def test_invalid_insurance_id(self, mock_select):
        # Mocking the database.select function to return None for account_id
        mock_select.return_value = None

        # Invalid insurance ID
        result = validate_credentials("TT654321XY", "password", MagicMock())

        # Assertions
        self.assertIsNone(result)
        self.assertEqual(mock_select.call_count, 1)  # Ensure database.select was called once

    @patch("account.database.select")
    @patch("account.key_storage.get_fernet_key")
    @patch("account.encryption.decrypt_password")
    def test_invalid_password(self, mock_decrypt_password, mock_get_fernet_key, mock_select):
        # Mocking the database.select function to return expected values
        mock_select.side_effect = [1, "encrypted_password"]

        # Mocking key_storage.get_fernet_key
        mock_get_fernet_key.return_value = b'fernet_key'

        # Mocking encryption.decrypt_password
        mock_decrypt_password.return_value = "33LondonEye!"

        # Invalid password
        result = validate_credentials("TT654321X", "33LondonEye", MagicMock())

        # Assertions
        self.assertIsNone(result)
        self.assertEqual(mock_select.call_count, 2)  # Ensure database.select was called twice

if __name__ == '__main__':
    unittest.main()
