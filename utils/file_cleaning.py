import shutil
import os


"""
file_cleaning.py -> every function related to the removal of residual selenium files in the program files (x86) directory (useless folders that store the browser data you accumulated while running the driver each bot session)
"""


# method to get the directory of the program files (x86)
def get_program_files_dir():
    """method to get the directory of the program files (x86)

    Args:
        None

    Returns:
        string: the directory of the program files (x86)

    """

    return os.environ["ProgramFiles(x86)"]


# method to get a list of all the files in a directory
def get_files_in_dir(dir):
    """method to get a list of all the files in a directory

    Args:
        None

    Returns:
        string[]: a list of all the files in a directory

    """
    return os.listdir(dir)


# method to delete a file
def delete_file(file):
    """method to delete a file

    Args:
        file (string): the file to delete

    Returns:
        None

    """
    shutil.rmtree(file)


# method to delete a list of files given a list of directories
def delete_files(files_to_delete):
    """method to delete a list of files given a list of directories

    Args:
        files (string[]): a list of directories of files to delete

    Returns:
        None

    """
    for file in files_to_delete:
        delete_file(file)
        print(f"Deleted file: {file}")
    print("Cached Selenium files cleared!")


# method to find a list of all the files that are selenium related in the programfiles (x86) directory
def get_directory_of_residual_selenium_files():
    """method to find a list of all the files that are selenium related in the programfiles (x86) directory

    Args:
        None

    Returns:
        string[]: a list of directories of files to delete

    """
    file_list_to_delete = []
    file_dir = get_program_files_dir()
    file_list = get_files_in_dir(file_dir)
    for file in file_list:
        if "scoped" in str(file):
            file_directory = os.path.join(file_dir, file)
            file_list_to_delete.append(file_directory)
    return file_list_to_delete


# main method to remove residual selenium files
def clean_selenium_files():
    """main method to remove residual selenium files

    Args:
        None

    Returns:
        None

    """
    files_to_delete = get_directory_of_residual_selenium_files()
    delete_files(files_to_delete)
