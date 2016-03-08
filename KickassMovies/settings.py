import getpass
import os
import pickle

import keyring


def load_settings():
    settings = open("KickassMoviesSettings.data", "rb")
    downloaded_movies_location = pickle.load(settings)
    users = pickle.load(settings)
    sleep_time = pickle.load(settings)
    email_address = pickle.load(settings)
    return downloaded_movies_location, users, sleep_time, email_address


def initial_setup():
    settings = open("KickassMoviesSettings.data", "wb")

    downloaded_movies_location = input("Filepath to completed movie download location: ")
    pickle.dump(downloaded_movies_location, settings)

    users = []
    for x in range(0, int(input("How many email addresses should be checked in the inbox: "))):
        users.append(input("Enter an email address:"))
    pickle.dump(users, settings)

    sleep_time = input("Sleep time after every run: ")
    pickle.dump(sleep_time, settings)

    email_address = input("Enter gmail address to check for emails: ")
    pickle.dump(email_address, settings)
    keyring.set_password("KickassMovies", email_address, getpass.getpass())

    return downloaded_movies_location, users, sleep_time, email_address

def change_settings():
    downloaded_movies_location, users, sleep_time, email_address = load_settings()
    os.remove("KickassMoviesSettings.data")
    keyring.delete_password("KickassMovies", email_address)
    initial_setup()