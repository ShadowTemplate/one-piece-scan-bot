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


op_bot_token = get_credential('op_bot_token')
personal_id = get_credential('personal_id')
group_id = get_credential('group_id')
telegram_chat_id = group_id
drive_client_id = get_credential('drive_client_id')
drive_client_secret = get_credential('drive_client_secret')
drive_refresh_token = get_credential('drive_refresh_token')
