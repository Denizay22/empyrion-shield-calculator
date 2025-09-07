#!/usr/bin/env python

import sys
import os
import argparse

def main():
    """
    Main entry point for the shield calculator. Parses command line arguments
    and launches either the GUI or command-line version based on user choice.
    """
    parser = argparse.ArgumentParser(description='Empyrion Shield Calculator')
    parser.add_argument('--cli', action='store_true', help='Run in command-line mode (default is GUI)')
    args = parser.parse_args()
    
    if args.cli:
        # Run command-line version
        from shieldcalc import main as cli_main
        cli_main()
    else:
        # Try to run the GUI version, fall back to CLI if PyQt6 is not available
        try:
            from shield_calculator_ui import main as ui_main
            ui_main()
        except ImportError:
            print("PyQt6 is not installed. Running in command-line mode instead.")
            print("To use the GUI, install PyQt6 with: pip install PyQt6")
            from shieldcalc import main as cli_main
            cli_main()

if __name__ == "__main__":
    main()
