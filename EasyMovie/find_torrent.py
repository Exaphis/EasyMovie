import subprocess, urllib, zlib
from bs4 import BeautifulSoup


def download_torrent(magnet_link):
    return subprocess.check_output(["transmission-remote", "-a", magnet_link])


def search_and_download(search_str, index=0):
    search_url = "http://kat.cr/usearch/" + search_str + " category:movies " + "is_safe:1" + "/"

    try: search = urllib.request.urlopen(search_url)
    except urllib.error.HTTPError: return ["No movies found", "No movies found"]

    search_soup = BeautifulSoup(zlib.decompress(search.read(), 15 + 32), "html.parser")

    titles = [title.getText() for title in search_soup.find_all(class_="cellMainLink")]
    magnets = [magnet.get('href') for magnet in search_soup.find_all(title="Torrent magnet link")]

    results = [{"title":title, "magnet":magnet} for title, magnet in zip(titles, magnets)]

    return [results[index]["title"], download_torrent(results[index]["magnet"])]