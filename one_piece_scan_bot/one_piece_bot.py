import telegram
import time

from one_piece_scan_bot.extractors import teams, artur
from one_piece_scan_bot.logger import get_application_logger
from one_piece_scan_bot.credentials import op_bot_token, telegram_chat_id

log = get_application_logger()
releases_to_check = ['One Piece']


def check_releases():
    log.info("Checking releases at " + str(time.strftime("%c")))
    for team in teams:
        log.info("Fetching releases from " + team.name + "...")
        try:
            releases, messages = team.fetch_f()
            for num, rel in enumerate(releases):
                if is_monitored(rel):
                    send_notification_if_needed(team, messages[num])
        except Exception as e:
            log.warning("Unable to fetch releases from " + team.name +
                        ". Going to skip it.")
            log.warning(e.message)


def check_artur():
    log.info("Checking The Library of Ohara at " + str(time.strftime("%c")))
    log.info("Fetching releases from " + artur.name + "...")
    try:
        releases, messages = artur.fetch_f()
        for num, rel in enumerate(releases):
            send_notification_if_needed(artur, messages[num], artur=True)
    except Exception as e:
        log.warning("Unable to fetch releases from " + artur.name +
                    ". Going to skip it.")
        log.warning(e.message)


def send_notification_if_needed(team, release, artur=False):
    # previous_namespace = namespace_manager.get_namespace()
    try:
        # namespace_manager.set_namespace(team.db_namespace)
        # item = ndb.Key('Release', release).get()
        item = None
        if not item:
            try:
                op_bot = telegram.Bot(token=op_bot_token)
                if artur:
                    message = "Hey, pirati! Nuova analisi disponibile!"
                else:
                    message = "Hey, pirati! Nuovo capitolo disponibile!"
                message += "\n\n" + team.name + ": " + release + "\n\nBuona lettura!"
                op_bot.sendMessage(chat_id=telegram_chat_id, text=message, disable_web_page_preview=True)
                # Release(id=release, name=release).put()
            except Exception as e:
                log.warning("Unable to send Telegram notification.")
                log.warning(e.message)
    except Exception as e:
        log.warning("Unable to store data on Datastore.")
        log.warning(e.message)
    finally:
        pass
        # namespace_manager.set_namespace(previous_namespace)


def get_status():
    return "ONE PIECE Scan Bot is running."


def is_monitored(manga):
    for release in releases_to_check:
        if release.lower() in manga.lower():
            return True
    return False
