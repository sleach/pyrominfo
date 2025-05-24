#!/usr/bin/env python3
"""
A simple command-line tool to parse ROM files and display their information.
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rominfo import RomInfo


def print_rom_info(props):
    """Print ROM information in a formatted way."""
    if not props:
        print("No ROM information found.")
        return

    print("\nROM Information:")
    print("-" * 50)
    for key, value in sorted(props.items()):
        if value:  # Only print non-empty values
            print(f"{key.replace('_', ' ').title()}: {value}")
    print("-" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Parse ROM files and display their information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Super Mario World.smc"
  %(prog)s "The Legend of Zelda.gb"
  %(prog)s "Sonic the Hedgehog.bin"
        """,
    )
    parser.add_argument("rom_file", help="Path to the ROM file to parse")
    args = parser.parse_args()

    try:
        props = RomInfo.parse(args.rom_file)
        print_rom_info(props)
    except FileNotFoundError:
        print(f"Error: File '{args.rom_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing ROM file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
