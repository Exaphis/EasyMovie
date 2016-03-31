import os
import hashlib
import urllib.parse
import urllib.request
import urllib.error

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


def search_and_download(folder_path):
    if os.path.isfile(folder_path):
        return [download_subtitles(folder_path)]

    videos = scan_for_movies(folder_path)

    output = []
    if False in videos:
        return ["Subtitles exist"]
    for video in videos:
        output.append(download_subtitles(video))

    return output
