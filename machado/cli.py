import argparse

from machado.commands.test import connection_test
from machado.config.initialize_env import main as initialize_main
from machado.commands.apply import main as apply_migrations
from machado.commands.new import main as new_migration

def main() -> None:
    parser = argparse.ArgumentParser(description="Database migration with style.")
    subparsers = parser.add_subparsers(dest="command")


    init_parser = subparsers.add_parser("init")
    init_parser.add_argument(
        "--path", type=str, default=".", help="Path to initialize."
    )

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("-v", "--version", type=str, help="Version to apply.")

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("-c", "--connection", action="store_true", help="Test connection with database.")

    new_migration_parser = subparsers.add_parser("new")

    new_migration_parser.add_argument(
        "type", choices=["sql", "py"], help="Type of migration script (sql or py)."
    )

    new_migration_parser.add_argument(
        "-m", "--message", type=str, required=True, help="Migration description."
    )

    args = parser.parse_args()

    if args.command == "init":
        initialize_main(args.path)
    if args.command == "test":
        if args.connection:
            connection_test()
    if args.command == "apply":
        apply_migrations()
    if args.command == "new":
        new_migration(args.type, args.message)
