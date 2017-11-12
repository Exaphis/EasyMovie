## Definitely does not work anymore after KAT was shut down.
Radarr is a much better alternative.

A small Python 3 script made to download movies from KickassTorrents easily. Checking an email address, it will use the subject line of unread emails to search KAT and download it with transmission-remote. 

## Installation

Download the KickassMovies folder.

## Usage

Run KickassMovies.py, and go through the initial setup. The settings will be saved as KickassMoviesSettings.data in the default Python working directory. Send an email from a specified user to your specified gmail account with the requested movie name in the subject line, and an email will be sent back to all of the users with the downloaded movie name and the transmission-remote output.

## Dependencies

* bs4 (BeautifulSoup)
* keyring
* yagmail

## To Do

* ~~Add automatic subtitle downloading~~
* ~~Be able to change settings~~
* Add GUI
