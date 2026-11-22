"""MANGA Plus rejects API calls without a SESSION-TOKEN header ("Account Banned"), which makes mloader
(used by lib/manganloader) crash with an IndexError. Any random UUID is accepted as token."""
import uuid

from mloader.loader import MangaLoader

_original_init = MangaLoader.__init__


def _init_with_session_token(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)
    self.session.headers["SESSION-TOKEN"] = str(uuid.uuid4())


MangaLoader.__init__ = _init_with_session_token
