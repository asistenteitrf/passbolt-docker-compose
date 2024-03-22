import logging
import os
import shutil
import datetime

class LogManager:
    def __init__(self, log_file='app.log', max_log_size_mb=10):
        self.log_file = log_file
        self.log_file_save = datetime.datetime.now().strftime("Salva_%Y_%m_%d_%H_%M_%S")     
        self.max_log_size_mb = max_log_size_mb
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler = logging.FileHandler(self.log_file)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.current_log_size_mb = os.path.getsize(self.log_file) / (1024 * 1024)  # Tamaño actual del archivo en MB
    
    def log_info(self, message):
        self.logger.info(message)
        self.check_log_size()
    
    def log_warning(self, message):
        self.logger.warning(message)
        self.check_log_size()
    
    def log_error(self, message):
        self.logger.error(message)
        self.check_log_size()
    
    def log_debug(self, message):
        self.logger.debug(message)
        self.check_log_size()
        
    def log_critical(self, message):
        self.logger.critical(message)
        self.check_log_size()
    
    def check_log_size(self):
        current_size_mb = os.path.getsize(self.log_file) / (1024 * 1024)
        if current_size_mb > self.max_log_size_mb:
            self.backup_logs()
    
    def backup_logs(self, backup_dir='log_backups'):
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        backup_file = os.path.join(backup_dir, f"{self.log_file_save}.bak")
        if os.path.exists(self.log_file):
            shutil.copy2(self.log_file, backup_file)
            self.logger.info(f"Logs salvados en: {backup_file}")
            open(self.log_file, 'w').close()  # Limpiar el archivo de logs
        else:
            self.logger.warning("No se encontró el archivo de logs para hacer la copia de seguridad.")

