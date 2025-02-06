import argparse

from machado.commands.test import connection_test
from machado.config.initialize_env import main as initialize_main

def main() -> None:
    parser = argparse.ArgumentParser(description="Database migration with style.")
    subparsers = parser.add_subparsers(dest="command")


    init_parser = subparsers.add_parser("init")
    init_parser.add_argument(
        "--path", type=str, default=".", help="Path to initialize."
    )

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("--version", type=str, help="Version to apply.")

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("--connection", action="store_true", help="Test connection with database.")

    new_migration_parser = subparsers.add_parser("new")

    group = new_migration_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sql", type=str, help="Initialize a new migration with SQL script.")
    group.add_argument("--py", type=str, help="Initialize a new migration with Python script.")


    args = parser.parse_args()

    if args.command == "init":
        initialize_main(args.path)
    if args.command == "test":
        if args.connection:
            connection_test()
    if args.command == "apply":
        # do X
        pass
    if args.command == "new":
        # do Y
        pass

