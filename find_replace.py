"""This program will crawl through files in a given directory
finding and replacing text in each file"""

import os
import time


def start():
    """All other functions will be called from here"""
    print(f'\nThe current working directory is "{os.getcwd()}"\n')
    change_cwd = str(input('Change this Directory? Y for Yes,'
                           ' anything else for No: '))

    # Proceed with CWD
    if change_cwd.lower() in ('y', 'yes'):
        get_folder_to_scan()
        print(f'\nThe current working directory is now "{os.getcwd()}"\n')

    # Or change CWD to the folder that contains the files that need scanned
    else:
        print(f'\nThe current working directory will stay "{os.getcwd()}"\n')

    # Discover what to find and replace with
    find, replacement = find_replace_text()

    # Build list of files to replace
    files_to_change = build_file_list_to_scan(find, replacement)

    # Function call to modify the files
    output_modified_files = modify_files(find, replacement, files_to_change)

    # Save list of files that were changed to disk
    save_to_disk(output_modified_files)

    # Exit program
    exit_program()


def get_folder_to_scan():
    """Change CWD to the folder that is to be scanned"""

    while True:
        # Path variable
        path = str(input('\nPlease enter the path where the files are stored.'
                         '\nOr enter "D" for your Documents folder.'
                         ' "Q" to quit. '))

        # If user wants to quit
        if path in ('Q', 'q'):
            exit_program()

        #  If user wants to default to the Documents folder
        if path in ('D', 'd'):
            if os.name == 'nt':  # Windows
                os.chdir(os.path.expanduser('~\\Documents'))
            else:
                os.chdir(os.path.expanduser('~/Documents'))
            break

        # Try the user input to see if it's valid
        try:
            os.chdir(path)
            break

        except FileNotFoundError:
            print("Path doesn't exist\n")


def find_replace_text():
    """Obtain the text to find and replace"""
    while True:
        find = str(input('\nWhat is the text you want to replace? '))
        replacement = str(input('What is the new text you want to add? '))
        keep_entries = str(input(f'\nReplace "{find}" with "{replacement}"'
                                 f'\nY for Yes, anything else for No '))
        if keep_entries.lower() in ('y', 'yes'):
            break

    return find, replacement


def build_file_list_to_scan(find, replacement):
    """Build a list of files to scan
    :Param: String find: text to find in the document
    :Param: String replacement: found text will be replaced
    """
    files_to_change = []

    # Specify file extension
    file_extension = str(input('\nSpecify the file extension of the files'
                               ' you wish to change: '))
    # Scan subdirectories too?
    scan_subdirectories = str(input('\nScan subdirectories too? "Y" '
                                    'for yes: '))

    # Add files to files_to_change list
    for path, _, filenames in os.walk("."):
        if path == '.':
            for file in filenames:
                if file.endswith(file_extension):
                    files_to_change.append(file)
        # Add entries from subdirectories
        if path != '.' and scan_subdirectories.casefold() == 'y':
            for file in filenames:
                if file.endswith(file_extension):
                    files_to_change.append(os.getcwd() +
                                           path[1::] + '/' + file)
    # Change '/' to '\' if on Windows
    if os.name == 'nt':
        renaming_list = []
        for file_name in files_to_change:
            file_name = file_name.replace('/', '\\')
            renaming_list.append(file_name)
        files_to_change = renaming_list

    # Proceed or exit
    if len(files_to_change) > 0:
        proceed_with_write = str(input(f'\nThe file(s)\n\n{files_to_change}'
                                       f'\n\nmay be modified.'
                                       f'\nAll text "{find}" '
                                       f'will be replaced with '
                                       f'"{replacement}".'
                                       f'\n\nIt\'s recommended that you have '
                                       f'a backup of the files that may be '
                                       f'modified.'
                                       f'\n\nDo you wish to proceed? '
                                       f'Y for yes, anything else to exit: '))
        # Exit program
        if proceed_with_write.casefold() != 'y':
            exit_program()

    else:
        print(f'\nThere are no files ending with '
              f'extension "{file_extension}."')
        exit_program()

    return files_to_change


def modify_files(find, replacement, files_to_change):
    """This function will write to disk
    :Param: String find: text to find in the document
    :Param: String replacement: found text will be replaced
    :Param: List files_to_change: files that will be scanned and modified
    if String find is found.
    """
    output_modified_file = ''

    # Overwrite only files that change
    for file_to_modify in files_to_change:
        with open(file_to_modify, 'r') as read_file:
            filedata = read_file.read()
        filedata_modified = filedata.replace(find, replacement)

        # If the file will change, proceed
        if filedata != filedata_modified:
            # Create a proper non I/O name
            file_to_overwrite = ''.join(file_to_modify)
            output_modified_file += file_to_modify + '\n'
            with open(file_to_overwrite, 'w') as filedata_changes:
                filedata_changes.write(f"{filedata_modified}")

    return output_modified_file


def save_to_disk(output_modified_file):
    """If files were modified save list to disk
    :Param: String output_modified_file: string with a list of all the files
    that was modified.
    """
    if len(output_modified_file) > 0:
        # Print the number of files changed
        changed_file_count = output_modified_file.count('\n')
        if changed_file_count == 1:
            print('\nThere was 1 file modified')
        else:
            print(f'\nThere were {changed_file_count} files modified.')
        print(f'\nThe list of changes are saved in folder'
              f' {os.getcwd()}, named "0_modified_files.txt".\n')
        with open('0_modified_files.txt', 'w') as modified_file_list:
            modified_file_list.write(f'{output_modified_file}')

    else:
        print('\nYour find/replace criteria yielded no changes. '
              'No files were modified.')


def exit_program():
    """Cleanly close program, giving time for reading outputs. Or go back to
    the main menu in file_manipulator

    """
    print('Do you want to return to the main menu?')
    return_to_file_manipulator = str(input('"Y" for yes. Anything else'
                                           ' for no. '))
    if return_to_file_manipulator.casefold() == 'y':
        return None
    print('\nHave a great day')
    time.sleep(5)
    raise SystemExit


if __name__ == "__main__":
    start()
