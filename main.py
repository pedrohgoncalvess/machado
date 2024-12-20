import argparse
import os
import shutil
import time


def main() -> None:
    parser = argparse.ArgumentParser(description="Database migration with style.")
    parser.add_argument("init", type=str, required=False, default=".")

    args = parser.parse_args()

    config_path = args.parser
    project_path = os.path.abspath(args.path)