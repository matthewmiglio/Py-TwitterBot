import shutil
import os


# method to get the directory of the program files (x86)
def get_program_files_dir():
    return os.environ["ProgramFiles(x86)"]


# method to get a list of all the files in a directory
def get_files_in_dir(dir):
    return os.listdir(dir)


# method to delete a file
def delete_file(file):
    shutil.rmtree(file)


# method to delete a list of files given a list of directories
def delete_files(files_to_delete):
    for file in files_to_delete:
        delete_file(file)
        print(f"Deleted file: {file}")
    print("Cached Selenium files cleared!")


# method to find a list of all the files that are selenium related in the programfiles (x86) directory
def get_directory_of_files_to_delete():
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
    files_to_delete = get_directory_of_files_to_delete()
    delete_files(files_to_delete)
