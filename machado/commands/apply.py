from machado.config.parser import ConfigParser
from machado.database.connection import Connection
from machado.database.parse_yaml import extract_sql_commands


def main():
    db_conn = Connection()
    main_config = ConfigParser()
    #project_configs = main_config.project_config()
    db_configs = main_config.database_config()

    with db_conn as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"select 1 from {db_configs.get('table_name')}")
        except Exception: # TODO: Specify errors
            conn.rollback()
            sql_commands = extract_sql_commands()
            for description, sql_command in sql_commands:
                cursor.execute(sql_command)
                print(f"[Machado]: {description}")
            conn.commit()

    print("[Machado]: Checking new migrations.")
