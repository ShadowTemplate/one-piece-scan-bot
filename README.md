# ONE PIECE Scan Bot

A Telegram bot to receive notifications when new ONE PIECE chapters are 
available. This bot periodically checks if new italian chapters are released on 
[MangaEden](https://www.mangaeden.com/it/) and [Juin Jutsu Team Forum](
http://juinjutsuteam.forumcommunity.net/). It is designed to be deployed on 
[Google App Engine](https://cloud.google.com/appengine/).


---
## Information

**Status**: `Actively maintained`

**Type**: `Personal project`

**Development year(s)**: `2016+`

**Authors**: [ShadowTemplate](https://github.com/ShadowTemplate)

**Notes**: *For personal use.* [optional]

---
## Getting Started

This bot is for personal use only, but you can create your own Google App 
Engine project and reuse it. Please create a *secrets.py* file and set these 
two values:

```
op_bot_token = "telegram_bot_token"
telegram_chat_id = "telegram_chat_id"
```

### Prerequisites

Clone the repository and install the required Python dependencies:

```
$ git clone https://github.com/ShadowTemplate/ONE-PIECE-scan-bot.git
$ cd ONE-PIECE-scan-bot
$ pip install --user -r requirements.txt
```

### Deployment

This repository includes the required Google App Engine libraries. The project 
is ready to be deployed.


---
## Building tools

* [Python 2.7](https://www.python.org/downloads/release/python-270/) - 
Programming language
* [Google App Engine](https://cloud.google.com/appengine/) - Web framework
* [pyquery](http://pyquery.readthedocs.io/en/latest/) - HTML parsing
* [python-telegram-bot](https://python-telegram-bot.org/) - Telegram API 
wrapper 

---
## Contributing

Any contribution is welcome. Feel free to open issues or submit pull requests.

---
## License

This project is licensed under the GNU GPLv3 license.
Please refer to the [LICENSE.md](LICENSE.md) file for details.

---
*This README.md complies with [this project template](
https://github.com/ShadowTemplate/project-template). Feel free to adopt it
and reuse it.*
