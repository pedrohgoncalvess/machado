import os
import re
from collections import defaultdict, deque

from machado.config.parser import ConfigParser
from machado.utils.path_config import project


def migrations_order():

    main_config = ConfigParser()
    project_configs = main_config.project_config()

    migration_dir_path = project_configs.get("migration_path")

    directory = f"{project}\\{migration_dir_path}"

    file_pattern = re.compile(r"^\d{10}-[A-Za-z0-9]{6}-[^.\n]+?\.(py|sql)$")

    id_pattern = re.compile(r"ID:\s*([A-Za-z0-9]{6})")
    after_pattern = re.compile(r"After:\s*([A-Za-z0-9]{6})")

    dependencies = defaultdict(set)
    all_ids = {}

    for file in os.listdir(directory):
        if not file_pattern.match(file):
            continue

        file_path = os.path.join(directory, file)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            id_match = id_pattern.search(content)
            after_match = after_pattern.search(content)

            if id_match:
                file_id = id_match.group(1)
                all_ids[file_id] = file

                after_id = after_match.group(1) if after_match else ""

                if after_id:
                    dependencies[after_id].add(file_id)
                else:
                    dependencies[file_id] = dependencies.get(file_id, set())


    sorted_ids = []
    in_degree = {k: 0 for k in all_ids}

    for after_id, dependents in dependencies.items():
        for dependent in dependents:
            in_degree[dependent] += 1

    queue = deque([file_id for file_id, degree in in_degree.items() if degree == 0])

    while queue:
        current_id = queue.popleft()
        sorted_ids.append(current_id)

        for dependent in dependencies[current_id]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    return sorted_ids
