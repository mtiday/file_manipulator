# file_manipulator
Program for manipulating files. This program will grow over time.
Menu items:
1. find_replace.py
Crawls through files in a given directory
finding and replacing text in each file
(Choose no when asked to copy any file that will be modified.
I'm working the kinks out of def backup_files_before_modification)

2. linux_name_checker.py
Crawls through a directory and lets you know if there are
names that will be considered duplicates in Windows. i.e. two folders
named example and Example in Linux would be the same folder in Windows.
Therefore if you copied this directory from Linux to Windows not
everything would copy.
