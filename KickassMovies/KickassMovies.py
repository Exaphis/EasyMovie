import os
import time
import datetime

import parse_movies
import find_torrent
import settings
from gmail import Gmail

if os.path.isfile("KickassMoviesSettings.data"):
    try:
        downloaded_movies_location, users, sleep_time, email_address, plex, filebot_location = settings.load_settings()
    except EOFError:
        os.remove("KickassMoviesSettings.data")
        downloaded_movies_location, users, sleep_time, email_address, plex, filebot_location = settings.initial_setup()
else:
    downloaded_movies_location, users, sleep_time, email_address, plex, filebot_location = settings.initial_setup()

if input("Would you like to change the settings? (y/n): ").lower() == "y":
    downloaded_movies_location, users, sleep_time, email_address, plex, filebot_location = settings.change_settings()

if plex:
    downloaded_movies_location = filebot_location

print_length = 50
new_movies_location = downloaded_movies_location
old_downloaded = os.listdir(downloaded_movies_location)

gmail = Gmail(email_address)
gmail.login_yagmail()

while True:
    current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print("Checking for emails" + " "*(print_length-(len("Checking for emails"))), end="\r")

    for received_email in gmail.get_unread():
        print("Email received" + " "*(print_length-(len("Email received"))))
        sender = received_email['From']
        subject = received_email['Subject']

        if any(email in sender for email in users):
            added_torrent = find_torrent.search_and_download(subject)

            print(" "*print_length)
            print(sender + " "*(print_length-(len(sender))))
            print(subject + " "*(print_length-(len(subject))))

            gmail.send_email(receivers=users, subject="Movie Received. Downloading.",
                             message="Added movie name: " + added_torrent[0] +
                                     "\nServer output: " + str(added_torrent[1]))

            print("Sent response email\n" + " "*(print_length-(len("Sent response email"))))

    parse_movies.cleanup(downloaded_movies_location)

    new_downloaded = os.listdir(downloaded_movies_location)
    successful_torrents = list(set(new_downloaded) - set(old_downloaded))

    for torrent in successful_torrents:
        parse_movies.parse(new_movies_location + "/" + torrent, plex, filebot_location)

        print(" " * print_length)
        print(torrent + " has been downloaded")
        print(" " * print_length)

        gmail.send_email(receivers=users, subject="Movie successfully downloaded",
                         message="Downloaded movie: " + torrent)

    old_downloaded = os.listdir(downloaded_movies_location)

    time.sleep(float(sleep_time))
