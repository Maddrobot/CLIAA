import logging
from datetime import datetime
import logging
import threading

class SingletonLogger:
    _instance = None
    _lock = threading.Lock()  # To ensure thread safety
    
    def __new__(cls, log_file_name="application.log", security_manager=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SingletonLogger, cls).__new__(cls)
                cls._instance.init_logger(log_file_name, security_manager)
        return cls._instance

    def init_logger(self, log_file_name, security_manager):
        self.logger = logging.getLogger('CLIAA')
        self.logger.setLevel(logging.DEBUG)
        
        fh = logging.FileHandler(log_file_name)
        fh.setLevel(logging.DEBUG)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(context)s - %(message)s')
        
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
        self.security_manager = security_manager

    def log(self, message, level, context="General"):
        encrypted_message = self.security_manager.encrypt_data(message) if self.security_manager else message

        if level == 'DEBUG':
            self.logger.debug(f"{context} - {encrypted_message}")
        elif level == 'INFO':
            self.logger.info(f"{context} - {encrypted_message}")
        elif level == 'WARNING':
            self.logger.warning(f"{context} - {encrypted_message}")
        elif level == 'ERROR':
            self.logger.error(f"{context} - {encrypted_message}")
        elif level == 'CRITICAL':
            self.logger.critical(f"{context} - {encrypted_message}")

    def secure_log(self, message, level="INFO"):
        # Implement any security measures here like encryption or sanitization
        sanitized_message = self.sanitize_message(message)
        self.log(sanitized_message, level)

    def sanitize_message(self, message):
        # Implement your sanitization logic here
        return message