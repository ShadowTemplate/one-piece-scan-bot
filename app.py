from flask import Flask, request
from timeit import default_timer as timer

from one_piece_scan_bot.logger import get_application_logger
from one_piece_scan_bot.one_piece_bot import check_artur, check_releases


log = get_application_logger()
app = Flask(__name__)


@app.before_request
def log_request_info():
    app.logger.debug(f"Headers: {request.headers}")
    app.logger.debug(f"Body: {request.get_data()}")


@app.route('/', methods=['GET'])
def main_get():
    return 'ONE PIECE Scan bot is running...'


@app.route('/release', methods=['GET'])
def _dummy_get():
    start_time = timer()
    # check_releases()
    # check_artur()
    msg = f"GET request completed in {str((timer() - start_time))} seconds."
    log.info(msg)
    return msg


@app.route('/test', methods=['GET'])
def test_get():
    start_time = timer()
    log.info(request)
    try:
        # do stuff
        log.info(f"GET request completed in {str((timer() - start_time))} seconds.")
        return 'TEST COMPLETED'
    except Exception as exc:
        return f"Okay, pirate, we've had a problem here.\n{type(exc).__name__}: {str(exc)}"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)  # threaded for multiple users access support
