import sys

from cx_Freeze import Executable, setup

product_name = "py-TwitterBot"

version = "0.1.0"


bdist_msi_options = {
    "upgrade_code": "{494bebef-6fc5-42e5-98c8-e63457934579}",
    "add_to_path": False,
    "initial_target_dir": f"[ProgramFilesFolder]\\{product_name}",
    "summary_data": {
        "author": "Matthew Miglio",
        "comments": "A bot for churning out Twitter followers",
        "keywords": "Twitter Follower Bot",
    },
}


base = "Win32GUI"   # for a GUI app
# base = None # None for console app

exe = Executable(
    script="tfc\\__main__.py",
    base=base,
    shortcut_name=f"{product_name} {version}",
    shortcut_dir="DesktopFolder",
    target_name=f"{product_name}.exe",
    copyright="2022 Matthew Miglio",
)

setup(
    name=product_name,
    description="Automatic Twitter Followers",
    executables=[exe],
    options={
        "bdist_msi": bdist_msi_options,
        
    },
)
