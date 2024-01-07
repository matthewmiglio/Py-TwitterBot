"""
This module defines the layout of the PyClashBot interface using PySimpleGUI.
"""

import os

import PySimpleGUI as sg
from PySimpleGUI import Window

sg.theme("Material2")
# Set the option to suppress error popups
sg.set_options(suppress_error_popups=True)


def stat_box(stat_name: str, size=(5, 1)) -> sg.Text:
    """Returns a pysimplegui text box object for stats layout"""
    return sg.Text(
        "0",
        key=stat_name,
        relief=sg.RELIEF_SUNKEN,
        text_color="blue",
        size=size,
    )


# fight stats


new_stats = [
    [
        sg.Frame(
            title="",
            expand_y=True,
            layout=[
                [
                    sg.Column([[sg.Text("Follows: ")], [sg.Text("Unfollows: ")]]),
                    sg.Column([[stat_box("follows")], [stat_box("unfollows")]]),
                ]
            ],
        ),
        sg.Frame(
            expand_y=True,
            title="",
            layout=[
                [
                    sg.Column(
                        [
                            [sg.Text("Current Following: ")],
                            [sg.Text("Current Followers: ")],
                        ]
                    ),
                    sg.Column(
                        [
                            [stat_box("bot_user_following_value")],
                            [stat_box("bot_user_follower_value")],
                        ]
                    ),
                ]
            ],
        ),
        sg.Frame(
            expand_y=True,
            title="",
            layout=[
                [
                    sg.Column(
                        [
                            [sg.Text("Blacklist count: ")],
                            [sg.Text("Whitelist count: ")],
                            [sg.Text("Greylist count: ")],
                        ]
                    ),
                    sg.Column(
                        [
                            [stat_box("blacklist_count")],
                            [stat_box("whitelist_count")],
                            [
                                stat_box("greylist_count"),
                            ],
                        ]
                    ),
                ]
            ],
        ),
        sg.Frame(
            expand_y=True,
            title="",
            layout=[
                [
                    sg.Column(
                        [
                            [sg.Text("Restarts: ")],
                        ]
                    ),
                    sg.Column(
                        [
                            [stat_box("restarts")],
                        ]
                    ),
                ]
            ],
        ),
    ],
    [
        sg.Frame(
            title="",
            expand_y=True,
            layout=[
                [
                    sg.Column(
                        [
                            [
                                sg.Text(
                                    "0",
                                    key="status",
                                    relief=sg.RELIEF_SUNKEN,
                                    text_color="blue",
                                    size=(60, 1),
                                ),
                            ],
                        ]
                    ),
                    sg.Text(
                        "0",
                        key="runtime",
                        relief=sg.RELIEF_SUNKEN,
                        text_color="blue",
                        size=(10, 1),
                    ),
                ]
            ],
        )
    ],
]


controls_layout = [
    [sg.Button("Start", key="start_button")],
]

plot_layout = [
    # PLOT IMAGE
    sg.Frame(
        title="",
        layout=[
            [
                sg.Image(
                    os.path.join(
                        os.environ["APPDATA"], "py-TwitterBot", "data_figure.png"
                    ),
                    key="data_figure",
                )
            ],
        ],
    ),
]

# main_layout = [stats, controls_layout, plot_layout]
main_layout = [new_stats, controls_layout, plot_layout]


def create_window() -> Window:
    """method for creating the main gui window"""
    return sg.Window(title="Twitterbot v0.0.1", layout=main_layout)
