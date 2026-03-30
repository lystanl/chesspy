#!/usr/bin/env python3
"""
Chess Tutor - Main Entry Point
A chess puzzle-solving tutor application.
"""

from ui_enhanced import ChessTutorUI


def main():
    """
    Main function to run the Chess Tutor application.
    """
    tutor = ChessTutorUI()
    tutor.run()


if __name__ == "__main__":
    main()
