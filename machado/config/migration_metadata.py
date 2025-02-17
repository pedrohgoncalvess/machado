import os
import re

from machado.config.parser import ConfigParser
from machado.utils.path_config import project


def migration_metadata(shortuuid: str) -> dict:
    """
    Searches for a file containing the specified shortUUID in its content
    and returns a dictionary with the following information:

    - ID: The shortUUID from the file.
    - Created at: The creation date/time of the file.
    - Description: The description provided in the file.
    - After: The ID of the file that this file depends on (if any).
    - User: The user associated with the file.

    The function only considers files that do not contain `.rollback` in their name
    and match the pattern of a timestamp, shortUUID, and file extension (.py or .sql).

    If the shortUUID is found in the file, the corresponding information is extracted.
    If no file matching the shortUUID is found, the function returns `None`.

    Args:
    shortuuid (str): The shortUUID to search for in the content of the files.

    Returns:
    dict: A dictionary containing the file's information (ID, Created at, Description, After, User).
          Returns `None` if no file with the given shortUUID is found.
    """

    main_config = ConfigParser()
    project_configs = main_config.project_config()

    migration_dir_path = project_configs.get("migration_path")

    directory = f"{project}\\{migration_dir_path}"

    file_pattern = re.compile(r"^\d{10}-[A-Za-z0-9]{6}-[^.\n]+?\.(py|sql)$")

    id_pattern = re.compile(r"ID:\s*([A-Za-z0-9]{6})")
    created_at_pattern = re.compile(r"Created at:\s*(.*)")
    description_pattern = re.compile(r"Description:\s*(.*)")
    after_pattern = re.compile(r"After:\s*(\S*)")
    user_pattern = re.compile(r"User:\s*(\S+)")

    for file in os.listdir(directory):
        if not file_pattern.match(file) or '.rollback' in file:
            continue

        file_path = os.path.join(directory, file)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            if shortuuid in content:
                id_match = id_pattern.search(content)
                created_at_match = created_at_pattern.search(content)
                description_match = description_pattern.search(content)
                after_match = after_pattern.search(content)
                user_match = user_pattern.search(content)

                file_info = {
                    "ID": id_match.group(1) if id_match else None,
                    "Created at": created_at_match.group(1) if created_at_match else None,
                    "Description": description_match.group(1) if description_match else None,
                    "After": after_match.group(1) if after_match else None,
                    "User": user_match.group(1) if user_match else None
                }

                return file_info

    return {}
