import logging.handlers

LOG_FILE = "test_log.log"
log_format = "[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d, %(funcName)s] %(message)s"
logging.basicConfig(filename=LOG_FILE,
                    filemode="w",
                    format=log_format,
                    level=logging.INFO)
time_hdls = logging.handlers.TimedRotatingFileHandler(
  LOG_FILE, when='D', interval=1, backupCount=7)
logging.getLogger().addHandler(time_hdls)

logging.info("begin service")

from pss_app import app
from waitress import serve

serve(app, host='0.0.0.0', port=8080, threads=30)  # WAITRESS!
