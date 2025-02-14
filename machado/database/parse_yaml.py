import yaml

from machado.config.parser import ConfigParser
from machado.database.connection import Connection
from machado.utils.path_config import project_root


def extract_sql_commands() -> list[tuple[str, str]]:
    """
    Extracts SQL commands and their descriptions from a YAML file.

    Returns:
        List of tuples containing (description, SQL command).
    """

    main_config = ConfigParser()
    db_configs = main_config.database_config()
    db_conn = Connection()

    with open(f"{project_root}\\database\\init-db.yaml", 'r') as file:
        yaml_content = yaml.safe_load(file)

    if db_conn.db_type in yaml_content and 'create-db-env' in yaml_content[db_conn.db_type]:
        commands = yaml_content[db_conn.db_type]['create-db-env']

        processed_commands = []

        for entry in commands:
            if isinstance(entry, dict) and "description" in entry and "command" in entry:
                description = entry["description"]
                command = entry["command"].format(table_name=db_configs.get("table_name"))
                processed_commands.append((description, command))

        return processed_commands

    return []
