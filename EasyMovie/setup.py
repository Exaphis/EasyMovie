import getpass
import pickle

import keyring


def load_settings():
    settings = open("settings.data", "r")
    downloaded_movies_location = pickle.load(settings)
    users = pickle.load(settings)
    sleep_time = pickle.load(settings)
    return downloaded_movies_location, users, sleep_time


def initial_setup():
    settings = open("settings.data", "wb")

    downloaded_movies_location = input("Filepath to completed movie download location: ")
    pickle.dump(downloaded_movies_location, settings)

    users = []
    for x in range(0, int(input("How many email addresses should be checked in the inbox: "))):
        users.append(input("Enter an email address:"))
    pickle.dump(users, settings)

    sleep_time = input("Sleep time after every run: ")
    pickle.dump(sleep_time, settings)

    email_address = input("Enter gmail address to check for emails: ")
    keyring.set_password("EasyMovie", email_address, getpass.getpass())

    return downloaded_movies_location, users, sleep_time, email_address
