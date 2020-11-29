import urlfetch
from pyquery import PyQuery

import re
import string

from one_piece_scan_bot.logger import get_application_logger

log = get_application_logger()


class Team:
    def __init__(self, name, fetch_f, namespace):
        self.name = name
        self.fetch_f = fetch_f
        self.db_namespace = namespace


def jjt_fetch():
    url = "https://jjtutility.herokuapp.com/tabReleases"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    }
    try:
        request = urlfetch.fetch(url, headers=headers)
        parser = PyQuery(request.content)
        releases = [r.attrib.get("title") for r in parser("a") if "One Piece" in r.attrib.get("title")]
        reader_url = "https://www.juinjutsureader.ovh/read/one-piece/it/0/{}/"
        chapter_numbers = [re.findall("(\d+)", r)[0] for r in releases]
        releases = [f"One Piece {ch} (ITA)" for ch in chapter_numbers]
        messages = [f"{r}\n{reader_url.format(ch_num)}" for r, ch_num in zip(releases, chapter_numbers)]
        log.info(releases)
        return releases, messages
    except Exception as exc:
        log.warning("Unable to fetch data.\nPlease check your Internet connection and the availability of the site.")
        log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")
        raise exc


def mangaeden_fetch():
    url = "https://www.mangaeden.com/it/it-manga/one-piece/"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    }
    try:
        request = urlfetch.fetch(url, headers=headers)
        parser = PyQuery(request.content)
        releases, messages = [], []
        base_url = 'https://www.mangaeden.com{}'
        for item in parser('.chapterLink'):
            chap_url = item.attrib['href']
            chapter_num = re.findall("(\d+)", chap_url)[0]
            releases.append(f"One Piece {chapter_num} (ITA)")
            messages.append(releases[-1] + "\n" + base_url.format(chap_url))
        log.info(releases)
        return releases, messages
    except Exception as exc:
        log.warning("Unable to fetch data.\nPlease check your Internet connection and the availability of the site.")
        log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")
        raise exc


def shueisha_fetch():
    # OP ENG has id 100020
    # web page: https://mangaplus.shueisha.co.jp/titles/100020
    url = "https://jumpg-webapi.tokyo-cdn.com/api/title_detail?title_id=100020"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like "
            "Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    try:
        request = urlfetch.fetch(url, headers=headers)
        raw_text = request.content
        clean_text = ''.join(chr(ch) for ch in raw_text if chr(ch) in string.printable)
        releases = re.findall("@R=#(\d+)", clean_text)  # will return only the last 3
        chapter_ids = re.findall("chapter/(\d+)/chapter_thumbnail", clean_text)[3:]
        reader_url = "https://mangaplus.shueisha.co.jp/viewer/{}"
        releases = ["One Piece " + r + " (ENG)" for r in releases]
        messages = [r + "\n" + reader_url.format(ch_id) for r, ch_id in zip(releases, chapter_ids)]
        log.info(releases)
        return releases, messages
    except Exception as exc:
        log.warning("Unable to fetch data.\nPlease check your Internet connection and the availability of the site.")
        log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")
        raise exc


def artur_fetch():
    url = "https://thelibraryofohara.com/"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like "
            "Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    try:
        request = urlfetch.fetch(url, headers=headers)
        parser = PyQuery(request.content)
        releases, messages = [], []
        for item in parser('.entry-title a'):
            article_url = item.attrib['href']
            article_name = item.text
            if "in-depth analysis" not in article_name:
                continue
            releases.append(article_name + " (ENG)")
            messages.append(releases[-1] + "\n" + article_url)
        log.info(releases)
        return releases, messages
    except Exception as exc:
        log.warning("Unable to fetch data.\nPlease check your Internet connection and the availability of the site.")
        log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")
        raise exc


jjt_team = Team("Juin Jutsu Team", jjt_fetch, "JJT")
mangaeden = Team("Mangaeden", mangaeden_fetch, "Mangaeden")
shueisha = Team("Shueisha", shueisha_fetch, "Shueisha")
artur = Team("Artur", artur_fetch, "Artur")

teams = [jjt_team, mangaeden, shueisha]
