import os
import shutil
from importlib import resources

from machado.config.parser import ConfigParser
from machado.database.connection import Connection
from machado.database.parse_yaml import extract_sql_commands


def main(migration_path: str) -> None:
    current_dir = os.path.abspath(".")
    project_name = os.path.basename(current_dir)

    config_file = os.path.join(current_dir, "machado.conf")

    if os.path.exists(config_file):
        print("[Machado]: Config file already exists.")
    else:
        with resources.path("machado.templates", "machado.conf") as config_template:
            shutil.copy2(str(config_template), config_file)

    migration_dir = os.path.join(migration_path, "migration")

    if os.path.exists(migration_dir):
        print("[Machado]: Migration directory already exists.")
    else:
        os.makedirs(migration_dir)

        try:
            with open(config_file, "r") as file:
                file_content = file.read()

            file_content = file_content.replace("$project_name$", project_name)
            file_content = file_content.replace("$migration_path$", migration_dir)

            with open(config_file, "w") as file:
                file.write(file_content)

            print(f"[Machado]: Configuration file created.")
            print(f"[Machado]: Migration directory created.")

        except Exception as error:
            if os.path.exists(config_file):
                os.remove(config_file)
            if os.path.exists(migration_dir):
                shutil.rmtree(migration_dir)
            raise error

    init_db()


def init_db() -> None:
    db_conn = Connection()
    main_config = ConfigParser()
    db_configs = main_config.database_config()

    with db_conn as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"select 1 from {db_configs.get('table_name')}")
            print("[Machado]: Machado table already exists.")
        except Exception as error: # TODO: Specify errors
            conn.rollback()
            sql_commands = extract_sql_commands()
            for description, sql_command, raise_if_exists in sql_commands:
                try:
                    cursor.execute(sql_command)
                    print(f"[Machado]: {description}")
                except Exception as err:
                    conn.rollback()
                    if raise_if_exists:
                        if err.__class__.__module__ == 'psycopg2.errors' and err.__class__.__name__ == 'UndefinedObject':
                            raise ValueError("[Machado]: Object already exists.")

            conn.commit()