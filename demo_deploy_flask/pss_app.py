import logging
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
  # 这样写日志
  logging.info("myendpoint We are computering now")
  return 'We are computering now'


@app.route('/server_status_code')
def server_status_code():
  """用于探活"""
  return "ok"
