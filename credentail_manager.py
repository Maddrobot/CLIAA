#pip instll keyring
import keyring
import logging

class CredentialManager:
    def __init__(self, service_name):
        self.service_name = service_name
        logging.basicConfig(filename='credential_manager.log', level=logging.INFO)

    def set_credential(self, username, password, user_role):
        if self.validate_user(user_role):
            try:
                encrypted_password = self.encrypt_data(password)  # Optionally add another encryption layer
                keyring.set_password(self.service_name, username, encrypted_password)
                logging.info(f"Credentials set for username: {username}")
            except Exception as e:
                logging.error(f"Error while setting credentials: {str(e)}")

    def get_credential(self, username, user_role):
        if self.validate_user(user_role):
            try:
                encrypted_password = keyring.get_password(self.service_name, username)
                if encrypted_password:
                    decrypted_password = self.decrypt_data(encrypted_password)  # Decrypt the password if you added an extra encryption layer
                    logging.info(f"Credentials retrieved for username: {username}")
                    return decrypted_password
                else:
                    logging.warning(f"No credentials found for username: {username}")
                    return None
            except Exception as e:
                logging.error(f"Error while retrieving credentials: {str(e)}")
                return None

    def delete_credential(self, username, user_role):
        if self.validate_user(user_role):
            try:
                keyring.delete_password(self.service_name, username)
                logging.info(f"Credentials deleted for username: {username}")
            except keyring.errors.PasswordDeleteError:
                logging.warning(f"No credentials found for deletion for username: {username}")
            except Exception as e:
                logging.error(f"Error while deleting credentials: {str(e)}")

    def validate_user(self, user_role):
        # Implement your user validation logic here
        # For demonstration, we'll allow all roles to access credentials
        return True

    def encrypt_data(self, data):
        # Implement additional encryption here if needed
        return data

    def decrypt_data(self, encrypted_data):
        # Implement decryption corresponding to your additional encryption
        return encrypted_data

if __name__ == '__main__':
    # Initialize CredentialManager with the name of the service for which you're storing credentials.
    credential_manager = CredentialManager("MyService")

    # Store credentials securely
    credential_manager.set_credential("my_username", "my_secure_password", "admin")

    # Retrieve stored credentials
    retrieved_password = credential_manager.get_credential("my_username", "admin")
    print(f"Retrieved password: {retrieved_password}")

    # Delete stored credentials
    credential_manager.delete_credential("my_username", "admin")