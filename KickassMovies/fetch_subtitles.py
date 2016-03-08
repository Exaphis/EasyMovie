import os
import subliminal
from babelfish import Language

subliminal.region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})


def scan_for_subtitle(folder):
    files = os.listdir(folder)
    for file in files:
        if '.srt' in os.path.splitext(file):
            return True

    for file in files:
        filepath = folder + "/" + file
        if os.path.isdir(filepath):
            if scan_for_subtitle(filepath) is True:
                return True

    return False


def save_subtitles(movie, subtitles):
    subliminal.save_subtitles(movie, subtitles)


def fetch_subtitles(folder):
    if scan_for_subtitle(folder) is True:
        return -1
    else:
        movies = subliminal.scan_videos(folder)

    return {'subtitles': subliminal.download_best_subtitles(movies, {Language('eng')}), 'movies': movies}
