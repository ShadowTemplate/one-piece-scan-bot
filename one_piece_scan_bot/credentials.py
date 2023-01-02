import os
from importlib import import_module

from one_piece_scan_bot.constants import SECRETS_UNTRACKED_FILE


def _get_credential_from_secrets(credential_key):
    try:  # will succeed locally if secret.py file is available
        secret_module = import_module(SECRETS_UNTRACKED_FILE.rstrip(".py"))
        return getattr(secret_module, credential_key)
    except ModuleNotFoundError:  # will fail on Heroku after deployments
        return None


def get_credential(credential_key):
    return os.environ.get(credential_key, _get_credential_from_secrets(credential_key))


OP_BOT_TOKEN = get_credential('OP_BOT_TOKEN')
PERSONAL_ID = get_credential('PERSONAL_ID')
GROUP_ID = get_credential('GROUP_ID')
TELEGRAM_CHAT_ID = GROUP_ID
DROPBOX_ACCESS_TOKEN = get_credential('DROPBOX_ACCESS_TOKEN')
DROPBOX_APP_KEY = get_credential('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET = get_credential('DROPBOX_APP_SECRET')
