import argparse

from machado.config.initialize_env import main as initialize_main


def main() -> None:
    parser = argparse.ArgumentParser(description="Database migration with style.")
    subparsers = parser.add_subparsers(dest='command')

    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('--path', type=str, default=".", help="Path to initialize.")
    
    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("--version", type=str, help="Version to apply.")
    
    args = parser.parse_args()
    
    if args.command == "init":
        initialize_main(args.path)
    if args.command == "apply":
        # faz X
        pass
    
