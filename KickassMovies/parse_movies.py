import os
import hashlib
import urllib.parse
import urllib.request
import urllib.error
import subprocess
import shutil
from threading import Timer

VIDEO_EXTENSIONS = ('.3g2', '.3gp', '.3gp2', '.3gpp', '.60d', '.ajp', '.asf', '.asx', '.avchd', '.avi', '.bik',
                    '.bix', '.box', '.cam', '.dat', '.divx', '.dmf', '.dv', '.dvr-ms', '.evo', '.flc', '.fli',
                    '.flic', '.flv', '.flx', '.gvi', '.gvp', '.h264', '.m1v', '.m2p', '.m2ts', '.m2v', '.m4e',
                    '.m4v', '.mjp', '.mjpeg', '.mjpg', '.mkv', '.moov', '.mov', '.movhd', '.movie', '.movx', '.mp4',
                    '.mpe', '.mpeg', '.mpg', '.mpv', '.mpv2', '.mxf', '.nsv', '.nut', '.ogg', '.ogm', '.omf', '.ps',
                    '.qt', '.ram', '.rm', '.rmvb', '.swf', '.ts', '.vfw', '.vid', '.video', '.viv', '.vivo', '.vob',
                    '.vro', '.wm', '.wmv', '.wmx', '.wrap', '.wvx', '.wx', '.x264', '.xvid')


def scan_for_movies(folder):
    files = os.listdir(folder)
    videos = []
    for file in files:
        if '.srt' in os.path.splitext(file):
            return [False]

    for file in files:
        filepath = folder + "/" + file
        if os.path.isdir(filepath):
            movies = scan_for_movies(filepath)
            if False in movies:
                return [False]
            else:
                for movie in movies:
                    videos.append(movie)

        if os.path.splitext(file)[1] in VIDEO_EXTENSIONS:
            videos.append(filepath)

    return videos


def get_hash(file):
    readsize = 64 * 1024
    with open(file, 'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def download_subtitles(filepath):
    user_agent = 'SubDB/1.0 (Exaphis; https://github.com/Exaphis/KickassMovies)'
    language = 'en'
    action = 'download'
    base_url = 'http://api.thesubdb.com/?'
    md5 = get_hash(filepath)

    content = {
        'action': action,
        'hash': md5,
        'language': language,
    }

    url = base_url + urllib.parse.urlencode(content)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', user_agent)
    try:
        res = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        return "Subtitle downloading failed"

    subtitles = res.read()
    subtitle_name = os.path.splitext(os.path.split(filepath)[1])[0] + ".srt"

    with open(os.path.split(filepath)[0] + subtitle_name, 'wb') as f:
        f.write(subtitles)

    return "Subtitle downloading succeeded"


def cleanup(folder_path):
    movies = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)) and
              os.path.splitext(file)[1] in VIDEO_EXTENSIONS]

    for movie in movies:
        os.makedirs(folder_path + "/" + os.path.splitext(movie)[0])
        os.rename(folder_path + "/" + movie, folder_path + "/" + os.path.splitext(movie)[0] + "/" + movie)


def delete_folder(folder):
    shutil.rmtree(folder)


def parse(folder_path, plex, filebot_path):
    if plex:
        subprocess.call(['filebot', '-get-missing-subtitles', folder_path])
        subprocess.call(['filebot', '-script', 'fn:amc', '--output', filebot_path, '--log-file', 'amc.log', '--action',
                         'copy', '-non-strict', '-extract', '-r', folder_path, '--def', 'excludeList=amc.txt'])

        t = Timer(259200.0, delete_folder)
        t.start()

    else:
        videos = scan_for_movies(folder_path)

        output = {}
        if False in videos:
            return {os.path.basename(folder_path): "Subtitles exist"}
        for video in videos:
            output[video] = (download_subtitles(video))