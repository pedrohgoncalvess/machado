import hashlib
import importlib.util
import sys
from datetime import datetime

from shortuuid import random

from machado.config.migration_metadata import migration_metadata
from machado.config.parser import ConfigParser
from machado.database.connection import Connection
from machado.utils.path_config import project


def run_migration(file_name: str) -> int:
    main_config = ConfigParser()
    project_configs = main_config.project_config()

    db_conn = Connection()

    db_conn.test_connection()

    migration_dir_path = project_configs.get("migration_path")

    file_path = f"{project}\\{migration_dir_path}\\{file_name}"
    migration_code = file_name.split("-")[1]

    file_type = file_path.split(".")[-1]

    if file_type not in ["py", "sql"]:
        raise TypeError(f"[Machado]: {file_name} has not valid migration format.")

    if file_type == "sql":
        with open(file_path, mode="r", encoding="utf-8") as file:
            statement = file.read()

    else:
        spec = importlib.util.spec_from_file_location("migration", file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["migration"] = module
        spec.loader.exec_module(module)

        variables_dict = {item: getattr(module, item) for item in dir(module)
                          if not item.startswith('__') and
                          not hasattr(__builtins__, item) and
                          not isinstance(getattr(module, item), type(importlib))}

        statement = ""
        for name, value in variables_dict.items():
            if type(value) == tuple:
                if len(value) > 1:
                    if callable(value[-1]):
                        metadata = value[-1]()
                        if metadata.get("valid_stmt"):
                            statement = f"{statement}\n {value[0]}"

    with db_conn as conn:
        cursor = conn.cursor()
        m_metadata = migration_metadata(migration_code)
        project_name = project_configs.get("name")

        db_conn.insert_migration(
            project_name,
            m_metadata.get("description"),
            migration_code,
            hashlib.sha256(statement.encode("utf-8")).hexdigest()
        )
        try:
            start = datetime.now()
            cursor.execute(statement)
            end = datetime.now()
            db_conn.change_migration_status(project_name, migration_code, "processed", (end - start))
            conn.commit()
            return 1
        except Exception as error:  # TODO: Specify errors
            conn.rollback()
            end = datetime.now()
            db_conn.change_migration_status(project_name, migration_code, "failed", (end - start))
            raise error
