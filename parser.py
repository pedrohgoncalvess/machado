"""
Configuration Parser Module.

This module handles the parsing of configuration files,
providing easy access to configuration settings across the application.
"""

import configparser
from typing import Any, Dict


class ConfigParser:
    """Configuration file parser that provides access to application settings."""

    def __init__(self, config_file: str = "machado.conf"):
        """
        Initialize the configuration parser.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self._load_config()

    def _load_config(self) -> None:
        """Load the configuration file."""
        try:
            self.config.read(self.config_file)
        except configparser.Error as e:
            raise Exception(f"Error reading config file: {e}")

    def default_config(self) -> Dict[str, Any]:
        """
        Get default configuration settings.

        Returns:
            Dict[str, Any]: Dictionary containing database settings.
        """
        database_config = self.config["Database"]
        return {
            "table_name": database_config["table_name"],
            "timeout": database_config["timeout"],
            "attempts": database_config["retry_attempts"]
        }

print(ConfigParser().default_config())