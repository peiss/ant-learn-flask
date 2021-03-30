import logging
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
  # 这样写日志
  logging.info("myendpoint We are computering now")
  return 'We are computering now'
