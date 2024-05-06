import unittest
from unittest.mock import MagicMock, patch
from account_setup import create_client, password_validation, insurance_id_format_validation, insurance_id_validation

# Mock the return value of the get_metadata().index method
account_instance = MagicMock()
account_instance.get_metadata.return_value = MagicMock(index=1)

class TestCreateClient(unittest.TestCase):
    def setUp(self):
        self.cursor = MagicMock()

    @patch("account_setup.wallet.wallet.create_account")
    @patch("account_setup.encryption.generate_key")
    @patch("account_setup.encryption.encrypt_password")
    @patch("account_setup.key_storage.store_fernet_key")
    @patch("account_setup.key_storage.store_keys")
    @patch("account_setup.database.update")
    @patch("account_setup.insurance_id_validation")
    def test_create_client_successful(self, mock_validation, mock_update, mock_store_keys, mock_store_fernet_key, mock_encrypt_password, mock_generate_key, mock_create_account):
        # Mock the return value of the get_metadata().index method
        account_instance = MagicMock()
        account_instance.get_metadata.return_value = MagicMock(index=1)
        
        mock_create_account.return_value = account_instance
        mock_generate_key.return_value = "fernet_key"
        mock_encrypt_password.return_value = "encrypted_password"
        mock_validation.return_value = 0

        # Run the function
        result = create_client("John", "Doe", "AB123456C", "Password123!", False, self.cursor)

        # Assertions and other test logic
        self.assertTrue(result)
        mock_create_account.assert_called_once()
        mock_generate_key.assert_called_once()
        mock_encrypt_password.assert_called_once_with("Password123!", "fernet_key")
        mock_store_fernet_key.assert_called_once_with("fernet_key", 1)
        mock_store_keys.assert_called_once()
        mock_update.assert_called_once()

    def test_create_client_invalid_password_format(self):
        result = password_validation("pass")  # Password less than 8 characters
        self.assertFalse(result)

        result = password_validation("password")  # No uppercase character
        self.assertFalse(result)

        result = password_validation("PASSWORD")  # No lowercase character
        self.assertFalse(result)

        result = password_validation("Password")  # No digit
        self.assertFalse(result)

        result = password_validation("Password!")  # No special character
        self.assertFalse(result)

    def test_create_client_invalid_insurance_id_format(self):
        result = insurance_id_format_validation("ABCD123456Z")  # Starts with invalid character
        self.assertFalse(result)

        result = insurance_id_format_validation("DF123456A")  # Starts with invalid characters
        self.assertFalse(result)

        result = insurance_id_format_validation("AB1234567")  # Too short
        self.assertFalse(result)

        result = insurance_id_format_validation("AB1234567Z")  # Too long
        self.assertFalse(result)

        result = insurance_id_format_validation("ABCD12345AZ")  # Invalid format
        self.assertFalse(result)

        result = insurance_id_format_validation("AB123456A")  # Valid format
        self.assertTrue(result)

    @patch("account_setup.database.select")
    def test_create_client_insurance_id_validation(self, mock_select):
        mock_select.return_value = 1
        result = insurance_id_validation("AB123456C", self.cursor)
        self.assertTrue(result)

        mock_select.return_value = 0
        result = insurance_id_validation("AB123456C", self.cursor)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
