import os

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image, ImageDraw, ImageFont

plot_png_dir = os.path.join(os.getenv("APPDATA"), "TwitterBot", "data_figure.png")


TEXT_SIZE = 15
WIDTH = 700
HEIGHT = 500


def parse_values(values):
    new_values = []
    for val in values:
        if "." in val:
            val = float(val)
            val = convert_time_to_datetime(val)
        if val != "":
            new_values.append(val)
        if val is False or val == "False":
            return False

    return new_values


def convert_time_to_datetime(time):
    return pd.to_datetime(time, unit="s")


def make_data():
    # get path of data file
    path = os.path.join(
        os.path.join(os.getenv("APPDATA"), "TwitterBot"), "bot_user_data.txt"
    )

    # Read data from the file
    with open(path, "r") as file:
        lines = file.readlines()

    # Process each line and create a list of dictionaries
    data_list = []
    for line in lines:
        if line == "\n" or line == " " or line == "":
            continue
        values = line.strip().split("NEW_DELIMITER")
        values = parse_values(values)

        if values is False:
            continue

        data_point = {
            "followers_value": int(values[0]),
            "time": pd.to_datetime(values[2], unit="s"),  # Convert to datetime
            "following_value": float(values[1]),
        }
        data_list.append(data_point)

    return data_list


def make_new_plot(mode="save"):
    try:
        # parse the data list into a dict
        print("Making plot...")
        data_list = make_data()

        # Create a DataFrame from the list of dictionaries and sort by the "time" column
        df = pd.DataFrame(data_list).sort_values(by="time")

        # make lines
        fig_followers = px.line(df, x="time", y="followers_value")
        fig_following = px.line(df, x="time", y="following_value")
        fig_following.update_traces(yaxis="y2")  # set to using secondary y axis

        ##make figure
        # make lines on a subplot with a secondary y axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_traces(fig_followers.data + fig_following.data)

        # edit the tick colors
        fig.update_layout(
            # x-axis
            xaxis=dict(tickfont=dict(size=TEXT_SIZE * 1.20)),
            # left y-axis
            yaxis=dict(tickfont=dict(size=TEXT_SIZE)),
            # right y-axis
            yaxis2=dict(tickfont=dict(size=TEXT_SIZE)),
        )

        # Add titles for axes
        fig.update_layout(
            xaxis_title=dict(
                text="Time",
                font=dict(family="Times New Roman", size=TEXT_SIZE, color="white"),
            ),
            yaxis_title=dict(
                text="Followers",
                font=dict(family="Times New Roman", size=TEXT_SIZE * 1.5, color="blue"),
            ),
            yaxis2_title=dict(
                text="Following",
                font=dict(
                    family="Times New Roman", size=TEXT_SIZE * 1.5, color="orange"
                ),
            ),
        )

        # color each line
        fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

        # if mode is show then show the figure in the browser, otherwise save with caching method
        if mode == "show":
            fig.show()
        elif mode == "save":
            save_plotly_figure(fig)
        else:
            print("Invalid mode param for make_new_plot_save()")
    except Exception as e:
        print(f"Failed making a plot: {e}")

    print("Created new plot")


# method to save a plotly figure as a png
def save_plotly_figure(fig):
    print(f"Saving plot to {plot_png_dir}...")
    print(fig.write_image(plot_png_dir, width=WIDTH, height=HEIGHT))
    print("Saved new plot!")


def make_empty_image():
    create_image_with_text(WIDTH, HEIGHT, plot_png_dir, "Empty data image")


def create_image_with_text(width, height, save_path, text):
    # Create an all-white image
    image = Image.new("RGB", (width, height), "white")

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Use a default font (change the font path if needed)
    font = ImageFont.truetype("arial.ttf", 50)

    # Calculate the position to center the text
    x = width / 2.5
    y = height / 2.5

    # Draw black text on the image
    draw.text((x, y), text, font=font, fill="black", align="center")

    # Save the image
    image.save(save_path)


def png_file_exists(file_path):
    # Check if the file exists and has a ".png" extension
    return os.path.exists(file_path) and file_path.lower().endswith(".png")


if not png_file_exists(plot_png_dir):
    print("Creating empty plot image...")
    make_empty_image()
    print("Created empty plot image")


# make_new_plot(mode="save")
# make_new_plot(mode="show")
