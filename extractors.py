from google.appengine.api import urlfetch
from pyquery import PyQuery
import logging as log


class Team:
    def __init__(self, name, fetch_f, namespace):
        self.name = name
        self.fetch_f = fetch_f
        self.db_namespace = namespace


def jjt_fetch():
    url = "http://juinjutsuteam.forumcommunity.net/?f=2385095"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    try:
        curr_chap = get_last_jjt_chapter()
        log.info("Current chapter: " + curr_chap)
        request = urlfetch.fetch(url, headers=headers)
        parser = PyQuery(request.content)
        discussions = parser(".big_list li:not(.annuncio) .bb h3 a")
        is_processable = lambda x: x.text and curr_chap in x.text
        get_text = lambda x: x.text.encode("utf-8")
        # the first discussion is related to RAW and would be a false positive
        releases = list(map(get_text, filter(is_processable, discussions[1:])))
        log.info(releases)
        return releases
    except Exception as e:
        log.warning("Unable to fetch data.\nPlease check your Internet connection and the availability of the site.")
        log.warning(e.message)
        raise e


def get_last_jjt_chapter():
    url = "http://juinjutsuteam.forumcommunity.net/"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    try:
        request = urlfetch.fetch(url, headers=headers)
        parser = PyQuery(request.content)
        home_title = parser("title")[0].text
        indicator = "One Piece"
        start_index = home_title.index(indicator) + len(indicator) + 1
        end_index = home_title.index(" ", start_index)
        return home_title[start_index:end_index]
    except Exception as e:
        log.warning(
            "Unable to fetch data.\nPlease check your Internet connection and the availability of the site.")
        log.warning(e.message)
        raise e


def mangaeden_fetch():
    url = "https://www.mangaeden.com/it/"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    try:
        request = urlfetch.fetch(url, headers=headers)
        parser = PyQuery(request.content)
        releases = []
        for item in parser('#news li div.hottestInfo'):
            item_parser = PyQuery(item)
            manga_name = item_parser(".mangaUrl")[0].text.encode("utf-8")
            for chapter_num in item_parser(".flagContainerDiv .chapterLink"):
                releases.append(manga_name + " " + chapter_num.text)
        log.info(releases)
        return releases
    except Exception as e:
        log.warning("Unable to fetch data.\nPlease check your Internet connection and the availability of the site.")
        log.warning(e.message)
        raise e


jjt_team = Team("Juin Jutsu Team", jjt_fetch, "JJT")
mangaeden_team = Team("Mangaeden", mangaeden_fetch, "Mangaeden")

teams = [jjt_team, mangaeden_team]

