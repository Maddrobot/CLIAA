#pip install PyJWT
#pip install python-dotenv
#pip install pygeoip
#### You need to download a free version of the GeoIP database from MaxMind in .dat format.
#### Link for MaxMind: https://dev.maxmind.com/geoip/legacy/geolite/
from cryptography.fernet import Fernet
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import hashlib
import re
import subprocess
import os
import pygeoip

load_dotenv()

class SecurityManager:
    def __init__(self):
        # Fetch the cipher key from environment variables
        self.key = os.environ.get('CIPHER_KEY')
        if not self.key:
            raise ValueError("CIPHER_KEY must be set in environment variables")
        # Initialize the cipher suite with the fetched key
        self.cipher_suite = Fernet(self.key)
        self.last_failed_login = defaultdict(datetime)
        self.log_key = os.getenv('LOG_CIPHER_KEY', self.key)  # Fall back to general key if not set
        self.log_cipher_suite = Fernet(self.log_key)
        # Fetch the secret key from environment variables for JWT
        self.secret_key = os.environ.get('SECRET_KEY')
        if not self.secret_key:
            raise ValueError("SECRET_KEY must be set in environment variables")

        self.algorithm = "HS256"
        self.failed_logins = defaultdict(int)  # IP -> number of failed logins
        self.last_failed_login = defaultdict(datetime)  # IP -> last failed login time
        self.user_activity = defaultdict(list)  # userID -> list of action
    
    def generate_token(self, user_id, is_admin):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        payload = {
            "user_id": user_id,
            "is_admin": is_admin,
            "exp": expiration_time
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return True, payload  # Token is valid
        except jwt.ExpiredSignatureError:
            return False, "Token has expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"

    def authorize_access(self, request):
        token = request.get("token")
        endpoint = request.get("endpoint")
        method = request.get("method")
        ip_address = request.get("ip_address")
        # More attributes...      

        is_valid, payload_or_error = self.verify_token(token)
    
        if not is_valid:
            return False, payload_or_error  # Unauthorized, with the reason

        # Role-based access control
        role = payload_or_error.get("role")
        if role == "admin":
            return True, "Authorized as Admin"

        if role == "user":
            if endpoint == "/user_data" and method == "GET":
                return True, "Authorized for user data retrieval"
            else:
                return False, "Not authorized for this action"

        # Rate limiting (this is a simplified example; you'd have more complex logic in a real app)
        if self.failed_logins[ip_address] > 5:
            return False, "Rate limit exceeded"

        # Geographical restrictions (assuming you have a way to get the country from the IP)
        country = self.country_from_ip(ip_address)
        if country not in ["US", "CA"]:
            return False, "Not authorized from this location"
        else:
            return True, "Authorized"    

        # Time-based restrictions
        current_hour = datetime.datetime.now().hour
        if current_hour < 9 or current_hour > 17:
            return False, "Access not allowed outside of business hours"

         # If none of the conditions are met
        return False, "Not authorized"
    
    def country_from_ip(self, ip_address):
        geoip = pygeoip.GeoIP('path/to/GeoIP.dat')
        return geoip.country_name_by_addr(ip_address)
    
    #### REGULAR ENCRYPTION ####
    def encrypt_data(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    def store_user_password(self, user_password):
        encrypted_password = self.encrypt_data(user_password)
        # Now store this encrypted_password in your database

    def check_user_password(self, stored_encrypted_password, entered_password):
        decrypted_password = self.decrypt_data(stored_encrypted_password)
        return decrypted_password == entered_password

    #### LOG ENCRYPTION DEFINTIONS ####
    def encrypt_log_data(self, log_data):
        """
        Encrypt log data. This could be similar to encrypt_data but
        uses a different key specific for logs.
        """
        encrypted_log_data = self.log_cipher_suite.encrypt(log_data.encode())
        return encrypted_log_data.decode()  # decode to convert bytes to string

    def decrypt_log_data(self, encrypted_log_data):
        """
        Decrypt log data.
        """
        decrypted_log_data = self.log_cipher_suite.decrypt(encrypted_log_data.encode()).decode()
        return decrypted_log_data
    
    #### LOGS AUDITER ####
    def audit_logs(self, logs):
        alerts = []
        
        # 1. Log Inspection for Failed Logins
        failed_logins = [log for log in logs if "failed_login" in log["action"]]
        if len(failed_logins) > 5:
            alerts.append("Multiple failed login attempts detected.")
        
        # 2. Regular Expression Matching for SQL Injection
        for log in logs:
            if re.search(r"(DROP\s+TABLE|CREATE\s+TABLE|DELETE\s+FROM)", log.get("query", ""), re.I):
                alerts.append(f"Potential SQL Injection detected in query: {log['query']}")
        
        # 3. Timestamp Analysis (assuming the logs have a datetime field in '%Y-%m-%d %H:%M:%S' format)
        late_night_activity = [log for log in logs if int(log["datetime"].split()[1].split(':')[0]) >= 22]
        if late_night_activity:
            alerts.append("Unusual late-night activity detected.")
        
        for file_path, expected_hash in self.monitored_files.items():
            try:
                current_hash = self.compute_file_hash(file_path)
                if current_hash != expected_hash:
                    alerts.append(f"Unauthorized changes detected in {file_path}.")
            except FileNotFoundError:
                alerts.append(f"{file_path} not found. It may have been deleted.")
        
        return alerts

    monitored_files = {
        #"/path/to/system/file": "expected_hash_value",
        #"/path/to/config/file": "another_expected_hash_value",
        # Add more files to monitor here
    }

    def compute_file_hash(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    def detect_threat(self, activity_log):
        ip_address = activity_log.get("ip_address")
        user_id = activity_log.get("user_id")
        action = activity_log.get("action")
        
        # Check for brute-force attacks by monitoring failed logins
        if action == "failed_login":
            self.failed_logins[ip_address] += 1
            self.last_failed_login[ip_address] = datetime.now()
            
            if self.failed_logins[ip_address] > 5:
                time_since_first_fail = datetime.now() - self.last_failed_login[ip_address]
                if time_since_first_fail < timedelta(minutes=5):
                    return "Potential brute-force attack detected from IP: {}".format(ip_address)
        
        # Check for unusual user activity
        self.user_activity[user_id].append(action)
        
        if self.user_activity[user_id].count("delete_record") > 10:
            return "Unusual number of deletions detected for user: {}".format(user_id)
        
        # Rate limiting (Here, more than 20 requests within a minute is considered an attack)
        if len([x for x in self.user_activity[user_id] if x == "request"]) > 20:
            return "Rate limit exceeded for user: {}".format(user_id)
        
        return "No threats detected"

    def apply_os_updates(self):
        # This is just a placeholder. The actual command will depend on your OS.
        subprocess.run(["apt-get", "update"])
        subprocess.run(["apt-get", "upgrade"])

    def update_application(self):
        # Logic to update your application, perhaps by pulling the latest version from a repository
        pass

    def update_firewall_rules(self):
        # Logic to update firewall rules, perhaps by downloading a new set of rules from a trusted source
        pass


    def apply_updates(self):
        alerts = []
        
        try:
            self.apply_os_updates()
            alerts.append("OS updated successfully.")
        except Exception as e:
            alerts.append(f"Failed to update OS: {str(e)}")

        try:
            self.update_application()
            alerts.append("Application updated successfully.")
        except Exception as e:
            alerts.append(f"Failed to update application: {str(e)}")

        try:
            self.update_firewall_rules()
            alerts.append("Firewall rules updated successfully.")
        except Exception as e:
            alerts.append(f"Failed to update firewall rules: {str(e)}")

        return alerts