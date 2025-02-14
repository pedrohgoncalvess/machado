"""
Configuration Parser Module.

This module handles the parsing of configuration files,
providing easy access to configuration settings across the application.
"""

import configparser
import os.path
from configparser import NoSectionError


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
        self._load_config_()

        if not os.path.exists(config_file):
            raise Exception("Configuration file not found. Try machado init command.")

    def _load_config_(self) -> None:
        """Load the configuration file."""
        try:
            self.config.read(self.config_file)
        except FileNotFoundError as _:
            raise Exception("Configuration file not found. Try machado init command.")
        except configparser.Error as e:
            raise Exception(f"Error reading config file: {e}")

    def project_config(self) -> dict[str, any]:
        """
        Get project configuration settings.

        Returns:
            dict[str, any]: Dictionary containing database settings.
        """
        project_config = self.config["project"]
        return {
            "name": project_config["name"],
            "migration_path": project_config["migration_path"]
        }

    def database_config(self) -> dict[str, any]:
        """
        Get database configuration settings.

        Returns:
            dict[str, any]: Dictionary containing database settings.
        """
        try:
            database_config = self.config["database"]
            return {
                "table_name": database_config.get("table_name", "machado"),
                "timeout": database_config.get("timeout", "20"),
                "attempts": database_config.get("retry_attempts", "3"),
                "driver": database_config.get("driver"),
                "port": database_config.get("port", "5432"),
                "host": database_config.get("host", "localhost"),
                "name": database_config.get("name", "postgres"),
                "user": database_config.get("user", "postgres"),
                "password": database_config.get("password", "admin")
            }
        except (NoSectionError, KeyError) as _:
            return {}