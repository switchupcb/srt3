#!/usr/bin/python3

import os
import sys
import importlib


def commands():
    commands = set()
    folder_path = os.path.normpath(os.path.join(__file__, os.pardir))
    for script in os.listdir(folder_path):
        if not script.startswith("_") and script.endswith(".py"):
            commands.add(script[:-3])
    return sorted(commands)


def show_help():
    print(
        "Available commands "
        "(pass --help to a specific command for usage information):\n"
    )
    for command in commands():
        print(f"- {command}")


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        show_help()
        sys.exit(0)

    command = sys.argv[1]
    if command not in commands():
        print(f'Unknown command: "{command}"')
        show_help()
        sys.exit(1)

    sys.argv = sys.argv[1:]
    module = importlib.import_module("srt.tools." + command, "")
    module.main()


if __name__ == "__main__":  # pragma: no cover
    main()
