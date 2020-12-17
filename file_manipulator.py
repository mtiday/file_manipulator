"""This program scans, reads, writes, modifies, creates, re-names files.
I expect this program to grow as I, and the community, grows.
"""

import time
import linux_name_checker
import find_replace


def start():
    """Get user input and execute actions on files and folders"""
    while True:
        print('\nPlease choose from the following list:')
        print('"1" to find and replace text in text files')
        print('"2" to scan Linux folders for files that would cause '
              'duplicates if copied to Windows.')
        program_to_open = str(input('"Q" to quit and end the program. '))

        if program_to_open in ('Q', 'q'):
            exit_program()
        elif program_to_open == '1':
            find_replace.start()
        elif program_to_open == '2':
            linux_name_checker.start()

        else:
            print(f'\n"{program_to_open}" wasn\'t a valid entry. '
                  f'please try again.\n')


def exit_program():
    """Exit the program cleanly."""
    print('\nHave a great day!!')
    time.sleep(5)
    raise SystemExit


if __name__ == "__main__":
    start()

