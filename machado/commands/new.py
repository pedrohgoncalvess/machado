import time
import re
from datetime import datetime

import shortuuid

from machado.config.parser import ConfigParser
from machado.utils.path_config import project_root, project


def main(migration_type: str, message: str) -> None:
    main_config = ConfigParser()
    project_configs = main_config.project_config()

    new_code = shortuuid.ShortUUID().random(length=6)

    migration_dir_path = project_configs.get("migration_path")

    template_path = f"{project_root}\\templates\\new_migration.{migration_type}"

    with open(template_path, mode='r') as file:
        content = file.read()

    tt_content = (content.
        replace("$id", new_code).
        replace("$description", message).
        replace("$datetime", datetime.now().strftime("%Y-%m-%d %H:%M:%S")).
        replace("$after", "TODO").
        replace("$user", "TODO")
    )

    tt_message = re.sub(r'[^a-zA-Z0-9]+', '_', message)
    new_file_name = f"{int(time.time())}-{new_code}-{tt_message}.{migration_type}"
    migration_path = f"{project}\\{migration_dir_path}\\{new_file_name}"

    if migration_type == "py":
        migration_config = main_config.migration_config()
        py_example = migration_config.get("py_example")

        tt_content = tt_content.split('''"$example sep$"''')[0] if not py_example else tt_content.replace('''"$example sep$"''', "")

        with open(migration_path, mode='w') as file:
            file.write(tt_content)
            print(f"[Machado]: New migration .{migration_type} created. ID: {new_code}.")
            return

    with open(migration_path, mode='w') as file:
        file.write(tt_content)
        print(f"[Machado]: New migration .{migration_type} created. ID: {new_code}.")
        return
