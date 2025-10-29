"""
Logging Configuration Module
Provides centralized logging setup for the entire application
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional
import sys


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        """Add color codes to log messages for console output"""
        if not sys.stderr.isatty():
            return super().format(record)
        
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logger(
    name: str = 'crypto_dashboard',
    level: str = 'INFO',
    log_dir: Optional[str] = None,
    enable_file: bool = True,
    enable_console: bool = True
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (defaults to 'logs' in project root)
        enable_file: Whether to enable file logging
        enable_console: Whether to enable console logging
    
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler with colored output
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler with rotation
    if enable_file:
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log file name with date
        log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
        
        # Rotating file handler (max 10MB, keep 5 backups)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = 'crypto_dashboard') -> logging.Logger:
    """
    Get or create a logger instance
    
    Args:
        name: Logger name
    
    Returns:
        logging.Logger: Logger instance
    """
    logger = logging.getLogger(name)
    
    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        return setup_logger(name)
    
    return logger


# Create module-specific loggers
def get_module_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module
    
    Args:
        module_name: Name of the module
    
    Returns:
        logging.Logger: Module-specific logger
    """
    return get_logger(f'crypto_dashboard.{module_name}')


# Convenience functions for quick logging
class LoggingMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self):
        """Get logger for the current class"""
        if not hasattr(self, '_logger'):
            self._logger = get_module_logger(self.__class__.__module__)
        return self._logger
    
    def log_debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def log_info(self, message: str, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)
    
    def log_warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def log_error(self, message: str, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)
    
    def log_critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self.logger.critical(message, *args, **kwargs)


# Set up default logger
default_logger = setup_logger(
    'crypto_dashboard',
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    enable_file=os.environ.get('ENABLE_FILE_LOGGING', 'true').lower() == 'true',
    enable_console=os.environ.get('ENABLE_CONSOLE_LOGGING', 'true').lower() == 'true'
)


# Utility functions for common logging scenarios
def log_api_call(endpoint: str, params: dict = None, response_code: int = None):
    """Log API call details"""
    logger = get_module_logger('api')
    if response_code and response_code >= 400:
        logger.error(f"API call failed: {endpoint} - Status: {response_code} - Params: {params}")
    else:
        logger.info(f"API call: {endpoint} - Status: {response_code} - Params: {params}")


def log_database_operation(operation: str, table: str, success: bool, details: str = None):
    """Log database operation"""
    logger = get_module_logger('database')
    if success:
        logger.info(f"Database {operation} on {table}: SUCCESS - {details or ''}")
    else:
        logger.error(f"Database {operation} on {table}: FAILED - {details or ''}")


def log_calculation_error(function_name: str, error: Exception, data_info: str = None):
    """Log calculation errors"""
    logger = get_module_logger('calculations')
    logger.error(f"Calculation error in {function_name}: {error} - Data: {data_info or 'N/A'}")


def log_user_action(user_id: str, action: str, details: dict = None):
    """Log user actions for audit"""
    logger = get_module_logger('audit')
    logger.info(f"User {user_id} performed {action} - Details: {details or {}}")


# Export main components
__all__ = [
    'setup_logger',
    'get_logger',
    'get_module_logger',
    'LoggingMixin',
    'log_api_call',
    'log_database_operation',
    'log_calculation_error',
    'log_user_action',
    'default_logger'
]
