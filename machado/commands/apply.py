from machado.config.migration_metadata import migration_metadata
from machado.config.migrations_order import migrations_order
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
            cursor.execute(f"select * from {db_configs.get('table_name')}")
            migrations = cursor.fetchall()
        except Exception: # TODO: Specify errors
            conn.rollback()
            sql_commands = extract_sql_commands()
            for description, sql_command in sql_commands:
                cursor.execute(sql_command)
                print(f"[Machado]: {description}")
            conn.commit()

    print("[Machado]: Checking new migrations.")

    migration_order = migrations_order()
    applied_migrations = [row[3] for row in migrations]

    if not migrations:
        if not migration_order:
            print("[Machado]: No migrations founded. Create new migrations with machado new command.")
            return

    apply_all = None
    for id_migration in migration_order:
        if id_migration not in applied_migrations:
            migration_mt = migration_metadata(id_migration)

            if not apply_all:
                option = input(f"[Machado]: Do you want to apply {id_migration} migration? [Y, y, n]: ")
                while option not in ["y", "n", "Y"]:
                    option = input(f"[Machado]: Just answer with Y, y or n (Y: for all, y: yes for this, n: not for this and subsequent ones): ")

                if option == 'n':
                    return

                if option == "Y":
                    apply_all = True

            print(f"[Machado]: Applying migration: {id_migration}.")
