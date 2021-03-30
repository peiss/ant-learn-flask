import logging.handlers

LOG_FILE = "test_log.log"
log_format = "[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d, %(funcName)s] %(message)s"
logging.basicConfig(filename=LOG_FILE,
                    filemode="a",
                    format=log_format,
                    level=logging.INFO)
time_hdls = logging.handlers.TimedRotatingFileHandler(
  LOG_FILE, when='D', interval=1, backupCount=7)
logging.getLogger().addHandler(time_hdls)

logging.info("begin service")

import requests
from pss_app import app
from waitress import serve

DEPLOY_PORT = 8889


def process_is_alive():
  """检测本地进程是否存在"""
  try:
    r = requests.get(f"http://127.0.0.1:{DEPLOY_PORT}/server_status_code")
    if r.status_code == 200 and r.text == "ok":
      return True
    return False
  except Exception as e:
    return False


if __name__ == "__main__":
  logging.info("try check and start app, begin")
  if process_is_alive():
    logging.info("process_is_alive_noneed_begin")
  else:
    logging.info("process_is_not_alive_begin_new")
    serve(app, host='0.0.0.0', port=DEPLOY_PORT, threads=30)  # WAITRESS!

  logging.info("try check and start app, end")
