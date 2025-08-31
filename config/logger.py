import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    """Clase para configurar el logger con rotacion de tamano."""
    def __init__(self):
        pass
    def setup(self, name="bcv_scrapping", log_level=logging.INFO):
        """Set up the logger configuration basado en tamano."""

        #Creamos el directorio logs si no existe
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        #Obtener el log
        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        # Para evitar duplicar handlers
        if logger.handlers:
            return logger
        
        # Handler con rotacion de tamano
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=10, 
            encoding='utf-8'
        )

        # Handler para la terminal
        console_handler = logging.StreamHandler()

        # Formateadores
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )

        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
    
    def get_logger(self, name="bcv_scrapping"):
        logger = logging.getLogger(name)
        if not logger.handlers:
            return self.setup(name)
        return logger