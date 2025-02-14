from machado.database.connection import Connection


def connection_test() -> None:

    db_conn = Connection()

    db_conn.connection()

    # TODO: Test DCL commands.
    print("[Machado]: Connection established with database.")
