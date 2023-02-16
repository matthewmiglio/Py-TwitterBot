import os
import PySimpleGUI as sg

from .stats import stat_box, stats

info_text = """Py-TwitterBot is a tool for gaining followers.
The program works by following users, then unfollowing them once following count reaches a threshold.
The program looks for targets by scraping the given list of accounts for their followers.
Matthew Miglio,  - Sept 2022"""

# defining various things that r gonna be in the gui.


main_layout = [
    # MAIN BOX
    [
        # LEFT SIDE BOX
        sg.Column(
            layout=[
                # INFORMATION TEXT BOX
                [
                    sg.Frame(
                        layout=[[sg.Text(info_text, size=(90, None))]],
                        title="Info",
                        relief=sg.RELIEF_SUNKEN,
                        expand_x=True,
                    )
                ],
                # STATS BOX
                [
                    sg.Frame(
                        layout=stats,
                        title="Stats",
                        relief=sg.RELIEF_SUNKEN,
                        expand_x=True,
                        expand_y=True
                    ),
                    sg.Frame(
                        layout=[
                            [
                                sg.Text("Following lower limit: "),
                                sg.InputText(
                                    key="following_lower_limit",
                                    default_text="100",
                                    enable_events=True,
                                    size=(7, 1),
                                ),
                            ],
                            [
                                sg.Text("Following upper limit: "),
                                sg.InputText(
                                    key="following_upper_limit",
                                    default_text="1000",
                                    enable_events=True,
                                    size=(7, 1),
                                ),
                            ],
                            [
                                sg.Text("Profiles to Scrape for Targets: "),
                                sg.InputText(
                                    key="profiles_to_scrape_for_targets",
                                    default_text="YourUsername, aPopularProfile, BarackObama",
                                    enable_events=True,
                                    size=(35, 2),
                                ),
                            ],
                            [
                                sg.Text("[DEV] Wait time between following: "),
                                sg.InputText(
                                    key="follow_wait_time",
                                    default_text="240",
                                    enable_events=True,
                                    size=(7, 1),
                                ),
                            ],
                            [
                                sg.Text("[DEV] Wait time between unfollowing: "),
                                sg.InputText(
                                    key="unfollow_wait_time",
                                    default_text="240",
                                    enable_events=True,
                                    size=(7, 1),
                                ),
                            ],
                            [
                                sg.Column(
                                    [
                                        [
                                            sg.Button("Start"),
                                            sg.Button("Stop", disabled=True),
                                            sg.Checkbox(
                                                text="Auto-start",
                                                key="autostart",
                                                default=False,
                                                enable_events=True,
                                            ),
                                        ]
                                    ],
                                    element_justification="left",
                                    expand_x=True,
                                ),
                                sg.Column(
                                    [
                                        [
                                            sg.Button("Help"),
                                            sg.Button("Issues?", key="issues-link"),
                                            sg.Button("Donate"),
                                        ]
                                    ],
                                    element_justification="right",
                                    expand_x=True,
                                ),
                            ],
                        ],
                        title="Controls",
                        relief=sg.RELIEF_SUNKEN,
                        expand_x=True,
                    )
                ],
                # PLOT IMAGE
                [
                    sg.Image(
                        os.path.join(
                            os.environ["APPDATA"], "py-TwitterBot", "data_figure.png"
                        ),
                        key="data_figure",
                    )
                ],
                # PROGRAM USER FOLLOWERS AND FOLLOWING STAT BOX
                [
                    # FOLLOWERS SECTIOn
                    sg.InputText(
                        "Followers", font=("Arial", 20), size=(11, 1), text_color="blue"
                    ),
                    sg.InputText(
                        "----",
                        font=("Arial", 20),
                        size=(6, 1),
                        text_color="blue",
                        key="current_followers",
                    ),
                    sg.InputText(
                        "----",
                        font=("Arial", 20),
                        size=(5, 1),
                        text_color="blue",
                        key="followers_change",
                    ),
                    # FOLLOWING SECTION
                    sg.InputText(
                        "Following", font=("Arial", 20), size=(11, 1), text_color="red"
                    ),
                    sg.InputText(
                        "----",
                        font=("Arial", 20),
                        size=(6, 1),
                        text_color="red",
                        key="current_following",
                    ),
                    sg.InputText(
                        "----",
                        font=("Arial", 20),
                        size=(5, 1),
                        text_color="red",
                        key="following_change",
                    ),
                ],
                # CONTROLS BOX
                [
                    
                ],
            ]
        ),
        # #RIGHT SIDE BOX
        # sg.Column(
        #     layout=[
        #         #PLOT IMAGE
        #         [
        #             sg.Image(
        #                 os.path.join(
        #                     os.environ["APPDATA"], "py-TwitterBot", "data_figure.png"
        #                 ),
        #                 key="data_figure",
        #             )
        #         ],
        #         #PROGRAM USER FOLLOWERS AND FOLLOWING STAT BOX
        #         [
        #             #FOLLOWERS SECTIOn
        #             sg.InputText('Followers',
        #                 font=("Arial", 20),
        #                 size=(11, 1),
        #                 text_color='blue'
        #                 ),
        #             sg.InputText('----',
        #                 font=("Arial", 20),
        #                 size=(6, 1),
        #                 text_color='blue',
        #                 key='current_followers'
        #                 ),
        #             sg.InputText('----',
        #                 font=("Arial", 20),
        #                 size=(5, 1),
        #                 text_color='blue',
        #                 key='followers_change'
        #                 ),
        #             #FOLLOWING SECTION
        #             sg.InputText('Following',
        #                 font=("Arial", 20),
        #                 size=(11, 1),
        #                 text_color='red'
        #                 ),
        #             sg.InputText('----',
        #                 font=("Arial", 20),
        #                 size=(6, 1),
        #                 text_color='red',
        #                 key='current_following'
        #                 ),
        #             sg.InputText('----',
        #                 font=("Arial", 20),
        #                 size=(5, 1),
        #                 text_color='red',
        #                 key='following_change'
        #                 ),
        #         ]
        #     ],
        #     element_justification='c',
        # ),
    ],
    # BOTTOM BOARDER BOX
    [
        stat_box("time_since_start", size=(7, 1)),
        sg.InputText(
            "Idle",
            key="current_state",
            use_readonly_for_disable=True,
            disabled=True,
            size=(11, 1),
            text_color="blue",
        ),
        sg.InputText(
            "Waiting for user start",
            key="current_status",
            use_readonly_for_disable=True,
            disabled=True,
            # text_color="blue",
            expand_x=True,
        ),
    ],
    # https://www.paypal.com/donate/?business=YE72ZEB3KWGVY&no_recurring=0&item_name=Support+my+projects%21&currency_code=USD
]

# a list of all the keys that contain user configuration
# user_config_keys = ["rows_to_target", "remove_offers_timer", "autostart"]
user_config_keys = [
    "following_lower_limit",
    "following_upper_limit",
    "profiles_to_scrape_for_targets",
    "follow_wait_time",
    "unfollow_wait_time",
    "autostart",
]

# list of button and checkbox keys to disable when the bot is running
disable_keys = user_config_keys + ["Start"]
