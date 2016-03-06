import time, find_torrent, os, gmail, keyring

downloaded_movies_location = "/home/kevin/Desktop/NAS/Movies/Downloaded Movies"
old_downloaded = os.listdir(downloaded_movies_location)
users = ["julieyueliu@gmail.com", "coachblueeagle@gmail.com", "kevin@kevinniuwu.com"]
print_length = 50
sleep_time = 60

gmail.login_imap()
gmail.login_yagmail()

while True:
    print("Checking for emails" + " "*(print_length-(len("Checking for emails"))), end="\r")

    for received_email in gmail.get_unread():
        print("Email received" + " "*(print_length-(len("Email received"))))
        sender = received_email['From']
        subject = received_email['Subject']

        if "julieyueliu@gmail.com" in sender or "coachblueeagle@gmail.com" in sender or "kevin@kevinniuwu.com" in sender:
            added_torrent = find_torrent.search_and_download(subject)

            print(" "*print_length)
            print(sender + " "*(print_length-(len(sender))))
            print(subject + " "*(print_length-(len(subject))))

            gmail.send_email(users, "Movie Received. Downloading.", "Added movie name: " + added_torrent[0] + "\nServer output: " + str(added_torrent[1]))
            print("Sent response email\n" + " "*(print_length-(len("Sent response email"))))

    new_downloaded = os.listdir(downloaded_movies_location)
    successful_torrents = list(set(new_downloaded) - set(old_downloaded))
    for torrent in successful_torrents:
        print(" "*print_length)
        print(torrent + " has been downloaded" + " "*(print_length-len(torrent + " has been downloaded")))
        gmail.send_email(users, "Success! Your movie has been downloaded.", "Downloaded movie name: " + torrent)
        print("Sent success email\n" + " "*(print_length-(len("Sent success email"))))
    old_downloaded = os.listdir(downloaded_movies_location)

    time.sleep(sleep_time)
