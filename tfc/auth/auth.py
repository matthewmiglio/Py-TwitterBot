import tweepy
from tfc.auth.auth_file_handler import get_creds






def make_api():
    creds=get_creds()
    
    consumer_key=creds[1]
    consumer_key_secret=creds[2]
    user_access_key=creds[3]
    access_secret_key=creds[4]

    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

    # set access to user's access key and access secret
    auth.set_access_token(user_access_key,access_secret_key)

    # calling the api
    api = tweepy.API(auth)

    return api

















