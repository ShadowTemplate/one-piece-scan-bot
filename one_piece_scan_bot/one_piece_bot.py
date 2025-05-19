import telegram
import time

from one_piece_scan_bot.constants import DROPBOX_BOT_DIR_PATH
from one_piece_scan_bot.dropbox_service import DropboxService
from one_piece_scan_bot.extractors import teams, artur
from one_piece_scan_bot.logger import get_application_logger
from one_piece_scan_bot.credentials import OP_BOT_TOKEN, TELEGRAM_CHAT_ID
from lib.manganloader.manganloader.docbuilder import Document

log = get_application_logger()
releases_to_check = ['One Piece']


class ContentChecker:

    def __init__(self):
        self.storage_service = DropboxService()
        self.team_items = {}

    def check_releases(self):
        log.info(f"Checking releases at {str(time.strftime('%c'))}")
        for team in teams:
            log.info(f"Fetching releases from {team.name}...")
            try:
                releases, messages = team.fetch_f()
                for release, message in zip(releases, messages):
                    if is_monitored(message):
                        self.send_notification_if_needed(team, release, message)
            except Exception as exc:
                log.warning(f"Unable to fetch releases from {team.name}. Going to skip it.")
                log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")

    def check_artur(self):
        log.info(f"Checking The Library of Ohara at {str(time.strftime('%c'))}")
        log.info(f"Fetching releases from {artur.name}...")
        try:
            releases, messages = artur.fetch_f()
            for release, message in zip(releases, messages):
                self.send_notification_if_needed(artur, release, message, artur_flag=True)
        except Exception as exc:
            log.warning(f"Unable to fetch releases from {artur.name}. Going to skip it.")
            log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")

    def send_notification_if_needed(self, team, release_code, release_message, artur_flag=False):
        file_dir = f"{DROPBOX_BOT_DIR_PATH}/{team.name}"
        try:
            if self._is_old_content(file_dir, release_code):
                return
            try:
                op_bot = telegram.Bot(token=OP_BOT_TOKEN)
                if artur_flag:
                    message = "Hey, pirati! Nuova analisi disponibile!"
                else:
                    message = "Hey, pirati! Nuovo capitolo disponibile!"
                message += f"\n\n{team.name}: {release_message}\n\nBuona lettura!"
                self.storage_service.create_file(f"{file_dir}/{release_code}")
                op_bot.sendMessage(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=message,
                    disable_web_page_preview=True,
                )
                try:
                    if team.name == "Shueisha":
                        chapter_title, url = release_message.split("\n")
                        doc = Document(
                            name=chapter_title,
                            source_url=url,
                            output_dir="/tmp/downloaded_chapters",
                            working_dir="/tmp/",
                            document_type='pdf')
                        doc.set_double_spread_version(want_double_spread_version=True)
                        doc_pdf = doc.build_from_url()
                        file_to_upload = doc_pdf.replace(".pdf", " double-spread.pdf")
                        op_bot.sendDocument(
                            chat_id=TELEGRAM_CHAT_ID,
                            document=open(file_to_upload, 'rb'),
                            caption=f"For {doc.get_device_name()}.",
                        )
                except Exception as exc:
                    log.warning("Unable to download and send Telegram chapter.")
                    log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")
                    op_bot.sendMessage(
                        chat_id=TELEGRAM_CHAT_ID,
                        text="Hey, pirati! La Marina ha sequestrato il capitolo: niente PDF questa settimana! ARRRWWW!",
                        disable_web_page_preview=True,
                    )
            except Exception as exc:
                log.warning("Unable to send Telegram notification.")
                log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")
        except Exception as exc:
            log.warning("Unable to store data.")
            log.warning(f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}")

    def _is_old_content(self, file_dir, file_name):
        if file_dir not in self.team_items:
            self.team_items[file_dir] = self.storage_service.list_files(file_dir)
        return any(item.name == file_name for item in self.team_items[file_dir])


def get_status():
    return "ONE PIECE Scan Bot is running."


def is_monitored(manga):
    for release in releases_to_check:
        if release.lower() in manga.lower():
            return True
    return False
