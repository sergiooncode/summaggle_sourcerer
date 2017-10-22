# -*- coding: utf-8 -*-
import os
from flask import Flask
from mongoengine import connect
import logging
from logging.handlers import RotatingFileHandler

from celery import Celery


app = Flask(__name__)

if os.environ.get('SOURCERER_SETTINGS'):
    app.config.from_envvar("SOURCERER_SETTINGS")
else:
    print("SOURCERER_SETTINGS environment not declared defaulting to the test environment...")
    app.config.from_pyfile(os.path.abspath('./config/config-local.py'))


connect(
    host=app.config['MONGODB_CONN_CHAIN']
)


formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(pathname)s %(funcName)s %(message)s")
log_handler = RotatingFileHandler(
    app.config['LOG_FILE_PATH'],
    mode='a',
    maxBytes=10*1024*1024,
    backupCount=1,
    encoding=None,
    delay=0
)
log_handler.setFormatter(formatter)
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(log_handler)
logger = logging.getLogger('summaggle')
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


# Initialize Celery
celery_app = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)
celery_app.conf.update(app.config)
celery_app.autodiscover_tasks([
    'sourcerer.tasks',
])


from sourcerer.cli import *
import sourcerer.views.views
