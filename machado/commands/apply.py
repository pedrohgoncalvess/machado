from machado.config.migration_metadata import migration_metadata
from machado.config.migration_order import migration_order
from machado.config.parser import ConfigParser
from machado.config.run_migration import run_migration
from machado.database.connection import Connection


def main():
    db_conn = Connection()
    main_config = ConfigParser()

    # TODO: CHECK ENVIRONMENT

    print("[Machado]: Checking new migrations.")

    m_order = migration_order()
    migrations = [] # TODO: CHECK MIGRATIONS TUPLE
    applied_migrations = [row[3] for row in migrations]

    if not migrations:
        if not migration_order:
            print("[Machado]: No migrations founded. Create new migrations with machado new command.")
            return

    apply_all = None
    for id_migration, file_name in m_order:
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

            try:
                run_migration(file_name)
                print(f"[Machado]: {id_migration} applied with successfully.")
            except Exception as error: # TODO: Specify errors
                print(f"[Machado]: Error while applying {id_migration} migration. \nError: {error.args}")
