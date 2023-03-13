# method to cache a line in a given file location
from utils.caching import _cache_data
import os

# method to get the appdata directory
def get_appdata_directory():
    """method to get the appdata directory

    Args:
        None

    Returns:
        string: the appdata directory

    """

    return os.getenv("APPDATA")


def cache_gui_theme(theme_string):
    path = get_appdata_directory() + r"\py-TwitterBot" + r"\gui_theme.txt"

    print(path)
    # _cache_data(data=theme_string, file_name)


cache_gui_theme("test")
