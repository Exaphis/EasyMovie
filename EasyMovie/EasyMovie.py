import os
import time

import find_torrent
import settings
from gmail import Gmail

if os.path.isfile("settings.data"):
    try:
        downloaded_movies_location, users, sleep_time, email_address = settings.load_settings()
    except EOFError:
        os.remove("settings.data")
        settings.initial_setup()
else:
    downloaded_movies_location, users, sleep_time, email_address = settings.initial_setup()

if input("Would you like to change the settings? (y/n): ").lower() == "y":
    settings.change_settings()

print_length = 50
old_downloaded = os.listdir(downloaded_movies_location)

gmail = Gmail(email_address)
gmail.login_imap()
gmail.login_yagmail()

while True:
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

            gmail.send_email(receivers=users, subject="Movie Received. Downloading.", message="Added movie name: " + added_torrent[0] + "\nServer output: " + str(added_torrent[1]))
            print("Sent response email\n" + " "*(print_length-(len("Sent response email"))))

    new_downloaded = os.listdir(downloaded_movies_location)
    successful_torrents = list(set(new_downloaded) - set(old_downloaded))
    for torrent in successful_torrents:
        print(" "*print_length)
        print(torrent + " has been downloaded" + " "*(print_length-len(torrent + " has been downloaded")))
        gmail.send_email(receivers=users, subject="Success! Your movie has been downloaded.", message="Downloaded movie name: " + torrent)
        print("Sent success email\n" + " "*(print_length-(len("Sent success email"))))
    old_downloaded = os.listdir(downloaded_movies_location)

    time.sleep(float(sleep_time))
