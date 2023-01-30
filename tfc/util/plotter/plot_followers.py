# given data following pattern value|date|time
# 1. read data from file
# 2. convert date and time to datetime as a column in a pandas dataframe
# 3. add value as a column in the dataframe
# 4. plot the data with plotly

import os

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import tfc.data

# PLOTTING THE DATA THAT IS SAVED IN follower_count_log.txt




def make_new_plot(mode='save'):
    #mode param: str -> 'save' or 'show;
        #saves to /appdata/roaming/py-twitterbot/data_figure.png

    # get path of data file
    path = (os.getenv('APPDATA')+r"\py-TwitterBot"+r"\data.txt")

    # make dataframe
    df = pd.read_csv(
        path,
        sep="|",
        header=None,
        names=["followers_value", "date", "time", "following_value"],
    )

    # parse date and time columns to a timestamp series
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])

    # make lines
    fig_followers = px.line(df, x="datetime", y="followers_value")
    fig_following = px.line(df, x="datetime", y="following_value")
    fig_following.update_traces(yaxis="y2")  # set to using secondary y axis

    ##make figure
    # make lines on a subplot with a secondary y axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_traces(fig_followers.data + fig_following.data)

    # configure axis titles
    fig.layout.xaxis.title = "Time"
    fig.layout.yaxis.title = "Followers"
    fig.layout.yaxis.color = "blue"
    fig.layout.yaxis2.title = "Following"
    fig.layout.yaxis2.color = "red"

    # color each line
    fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    #if mode is show then show the figure in browser
    if mode == 'show':
        fig.show()
    elif mode == 'save':
        save_plotly_figure(fig)
    else:
        print('invalid mode param for make_new_plot_save()')

#method to save a plotly figure as a png
def save_plotly_figure(fig):
    save_path=os.getenv("APPDATA")+r"\py-TwitterBot"+r'\data_figure.png'
    fig.write_image(save_path)


