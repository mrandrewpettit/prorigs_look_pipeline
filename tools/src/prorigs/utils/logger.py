import logging
import os, sys

from logging.handlers import RotatingFileHandler
from PySide2.QtGui import QTextCursor, QColor
from PySide2.QtWidgets import QTextEdit

class AppLogger:
    def __init__(self, log_file: str, log_level=logging.INFO):
        self.logger = logging.getLogger("ProRigsLogger")
        self.logger.setLevel(log_level)

        # File handler
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

        # Stream handler for GUI log_text_edit
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        self.logger.addHandler(console_handler)

        # Placeholder for text edit handler (added dynamically)
        self.text_handler = None

    def add_text_handler(self, text_widget):
        """Add a handler to log to a QTextEdit widget."""
        if not self.text_handler:
            self.text_handler = TextEditLogHandler(text_widget)
            self.logger.addHandler(self.text_handler)

    def log(self, message, level=logging.INFO):
        """Log messages with different severity levels."""
        log_method = {
            logging.DEBUG: self.logger.debug,
            logging.WARNING: self.logger.warning,
            logging.ERROR: self.logger.error,
            logging.INFO: self.logger.info,
        }.get(level, self.logger.info)

        log_method(message)

    def get_logger(self):
        """Provide access to the underlying logger instance."""
        return self.logger

class TextEditLogHandler(logging.Handler):
    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.text_edit = text_edit
        self.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))  # Log format


    def emit(self, record):
        msg = self.format(record)

        # Determine color based on log level
        if record.levelno == logging.DEBUG:
            color = QColor('blue')
        elif record.levelno == logging.INFO:
            color = QColor('white')
        elif record.levelno == logging.WARNING:
            color = QColor('orange')
        elif record.levelno == logging.ERROR:
            color = QColor('red')
        elif record.levelno == logging.CRITICAL:
            color = QColor('darkred')
        else:
            color = QColor('white')  # Default color
        
        # Insert the log message at the current cursor position
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.setCharFormat(cursor.charFormat())  # Store the current character format

        # Set the text color
        text_format = cursor.charFormat()
        text_format.setForeground(color)
        cursor.setCharFormat(text_format)

        # Append the formatted message
        cursor.insertText(msg + '\n')

        # Restore default character format
        cursor.setCharFormat(cursor.charFormat())
        self.text_edit.setTextCursor(cursor)