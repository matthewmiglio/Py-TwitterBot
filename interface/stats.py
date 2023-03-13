import PySimpleGUI as sg

from .theme import THEME

sg.theme(THEME)


def stat_box(stat_name: str, size=(5, 1)):
    return sg.Text(
        "0",
        key=stat_name,
        relief=sg.RELIEF_SUNKEN,
        text_color="white",
        size=size,
    )


stats_title = [
    [
        [
            sg.Text("Unfollows: "),
        ],
        [
            sg.Text("Follows: "),
        ],
        [
            sg.Text("Accounts Examined: "),
        ],
        [
            sg.Text("Targets Left: "),
        ],
        [
            sg.Text("New Targets: "),
        ],
    ],
    
]


stats_values = [
    [
        [
            stat_box("unfollows"),
        ],
        [
            stat_box("follows"),
        ],
        [
            stat_box("accounts_examined"),
        ],
        [
            stat_box("targets_left"),
        ],
        [
            stat_box("targets_added"),
        ],
    ],
    
]

stats = [
    [
        sg.Column(stats_title[0], element_justification="right"),
        sg.Column(stats_values[0], element_justification="left"),
    ]
]
