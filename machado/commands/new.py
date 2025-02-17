import time
import re
from datetime import datetime

import shortuuid

from machado.config.migrations_order import migrations_order
from machado.config.parser import ConfigParser
from machado.utils.path_config import project_root, project


def main(file_type: str, message: str) -> None:
    main_config = ConfigParser()
    project_configs = main_config.project_config()
    migration_conf = main_config.migration_config()

    new_code = shortuuid.ShortUUID().random(length=6)

    migration_dir_path = project_configs.get("migration_path")

    order = migrations_order()

    after = order[-1] if len(order) > 0 else None

    migration_types = ["migration", "rollback"]

    print(f"[Machado]: New ID migration: {new_code}")

    for migration_type in migration_types:
        template_path = f"{project_root}\\templates\\new_{migration_type}.{file_type}"

        with open(template_path, mode='r') as file:
            content = file.read()

        tt_content = (content.
            replace("$id_migration", new_code).
            replace("$id", new_code).
            replace("$description", message).
            replace("$datetime", datetime.now().strftime("%Y-%m-%d %H:%M:%S")).
            replace("$after", after if after else "").
            replace("$user", migration_conf.get("user"))
        )

        tt_message = re.sub(r'[^a-zA-Z0-9]+', '_', message)
        new_file_name = f"{int(time.time())}-{new_code}-{tt_message}.{'rollback.' if migration_type == 'rollback' else ''}{file_type}"
        migration_path = f"{project}\\{migration_dir_path}\\{new_file_name}"

        if file_type == "py":
            migration_config = main_config.migration_config()
            py_example = migration_config.get("py_example")

            tt_content = tt_content.split('''"$example sep$"''')[0] if not py_example else tt_content.replace('''"$example sep$"''', "")

        with open(migration_path, mode='w') as file:
            file.write(tt_content)
            print(f"[Machado]: File .{file_type} type {migration_type} created.")

    return
