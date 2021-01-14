"""This program will crawl through files in a given directory
finding and replacing text in each file
"""

import os
import time


# Main function
def start():
    """This program does bulk find/replace in text Files. All function
    calls are in if statements. When a user wants to return to the main
    program continue_executing wil be changed to False so that the
    program completes and returns to main.
    Program.
    :Param: Boolean continue_executing: Continue with function calls
    if the user doesn't want to quit
    :Param: String output_modified_files: Contains modifiable files
    :Param: String find: Contains characters to search for
    :Param: String replacement: Contains the replacement characters
    :Param: List files_to_change: Files that will be scanned for possible
     changes to be made
     """
    continue_executing = True
    output_modified_files = ''
    find = ''
    replacement = ''
    files_to_change = []

    print(f'\nThe current working directory is "{os.getcwd()}"\n')
    change_cwd = str(input('Change this Directory? Y for Yes,'
                           ' anything else for No: '))

    # Proceed with CWD
    if change_cwd.lower() in ('y', 'yes'):
        continue_executing = get_folder_to_scan()
        if continue_executing:
            print(f'\nThe current working directory is now "{os.getcwd()}"\n')

    # Change CWD to the folder that contains the files that need scanned
    else:
        print(f'\nThe current working directory will stay '
              f'"{os.getcwd()}"\n')

    # Discover what to find and replace with
    if continue_executing:
        find, replacement = find_replace_text()

    # Build list of files to replace
    if continue_executing:
        files_to_change = build_file_list_to_scan(find, replacement)
        if files_to_change == '':
            continue_executing = False

    # Change '/' to '\' in files_to_change if on Windows
    if continue_executing:
        if os.name == 'nt':
            files_to_change = os_is_windows(files_to_change)

    # Function call to modify the files
    if continue_executing:
        output_modified_files = \
            modify_files(find, replacement, files_to_change)

    # Save list of files that were changed to disk
    if continue_executing:
        save_list_of_changes(output_modified_files)

    # Exit program
    exit_program()


# Change CWD
def get_folder_to_scan():
    """Change CWD to the folder that is to be scanned"""
    while True:
        # Path variable
        path = str(input('\nPlease enter the path where the files are stored.'
                         '\nOr enter "D" for your Documents folder.'
                         ' "Q" to quit. '))

        # If user wants to quit
        if path in ('Q', 'q'):
            return False

        #  If user wants to default to the Documents folder
        if path in ('D', 'd'):
            if os.name == 'nt':  # Windows
                os.chdir(os.path.expanduser('~\\Documents'))
            else:
                os.chdir(os.path.expanduser('~/Documents'))
            return True

        # Try the user input to see if it's valid
        try:
            os.chdir(path)
            return True

        except FileNotFoundError:
            print("Path doesn't exist\n")


# Get the text to find and what to replace it with
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


# Create a list of files to scan through
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

    # Add entries from subdirectories, if requested
    if scan_subdirectories.casefold() == 'y':
        for path, _, filenames in os.walk("."):
            if path != '.':
                for file in filenames:
                    if file.endswith(file_extension):
                        files_to_change.append(os.getcwd() +
                                               path[1::] + '/' + file)

    # Proceed or exit
    if len(files_to_change) > 0:
        proceed = str(input(f'\nThe file(s)\n\n{files_to_change}\n\nmay be '
                            f'modified.\nAll text "{find}" will be replaced '
                            f'with "{replacement}".\n\n'
                            f'Do you wish to proceed? '
                            f'Y for yes, anything else to exit: '))
        # Exit program
        if proceed.casefold() != 'y':
            return ''
        return files_to_change

    print(f'\nThere are no files ending with extension "{file_extension}."\n')
    return ''


# Change occurrences of "/" to "\" if running on Windows
def os_is_windows(files_to_change):
    """Modify the "/" to "\" if running the program on a Windows OS
    :Param: List files_to_change: list of files that may be modified
    """
    windows_files_to_change = []
    for file_name in files_to_change:
        file_name = file_name.replace('/', '\\')
        windows_files_to_change.append(file_name)
    return windows_files_to_change


# If changes are made in a file, save the file to disk
def modify_files(find, replacement, files_to_change):
    """This function will write to disk
    :Param: String find: text to find in the document
    :Param: String replacement: found text will be replaced
    :Param: List files_to_change: files that will be scanned and modified
    if String find is found.
    """
    output_modified_file = ''
    backup_original_file = str(input('\n\nDo you want to copy any file that '
                                     'will be modified, before it is modified?'
                                     '\n"Y" for Yes anything else for no: '))
    # Overwrite only files that change
    if backup_original_file.casefold() == 'y':
        backup_files_before_modification(find, replacement, files_to_change)

    # Overwrite only files that change
    for file_to_modify in files_to_change:
        try:
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
        except UnicodeError:
            print(f"\n{file_to_modify} isn't a Text document.")
            print("The file won't be scanned")

    return output_modified_file


# Backup files before modification, if user desires
def backup_files_before_modification(find, replacement, files_to_change):
    """Backup files before modification
    :Param: String find: text to find in the document
    :Param: String replacement: found text to be replaced
    :Param: List files_to_change: files will be scanned for find/replace
    """
    # set directory to Desktop folder per Windows or non Windows
    if os.name == 'nt':
        output_modified_file = os.path.expanduser('~\\Desktop')
    else:
        output_modified_file = os.path.expanduser('~/Desktop')

    for file_to_modify in files_to_change:
        # Weed out non text files with the try
        try:
            with open(file_to_modify, 'r') as read_file:
                filedata = read_file.read()
            filedata_modified = filedata.replace(find, replacement)

            # If the file will change, make a copy
            if filedata != filedata_modified:
                # Add a slash if file_to_modify doesn't start with one
                if file_to_modify[0] not in ('/', '\\'):
                    if os.name == 'nt':
                        file_to_modify = os.getcwd() + '\\' + file_to_modify
                    else:
                        file_to_modify = os.getcwd() + '/' + file_to_modify

                file_to_backup = output_modified_file + file_to_modify
                path_of_file = os.path.dirname(file_to_backup)

                # Create path, if it doesn't exist
                if not os.path.isdir(path_of_file):
                    try:  # Create more than one directory
                        os.makedirs(path_of_file)
                    except AttributeError:  # Create one directory
                        os.mkdir(path_of_file)

                with open(file_to_backup, 'w') as filedata_changes:
                    filedata_changes.write(f"{filedata}")
        except UnicodeError:
            pass


# Save list of files changed to disk
def save_list_of_changes(output_modified_file):
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
              'No files were modified.\n')


# Exit program with an option of returning to main menu
def exit_program():
    """Cleanly close program, giving time for reading outputs. Or go back to
    the main menu in file_manipulator
    """
    print('\nDo you want to return to the main menu?')
    return_to_file_manipulator = str(input('"Y" for yes. Anything else'
                                           ' for no. '))
    if return_to_file_manipulator.casefold() != 'y':
        print('\nHave a great day')
        time.sleep(5)
        raise SystemExit


if __name__ == "__main__":
    start()
