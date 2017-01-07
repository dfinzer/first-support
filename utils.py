import os


def on_heroku():
    return 'DYNO' in os.environ