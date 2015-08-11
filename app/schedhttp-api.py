#!flask/bin/python
import logging
from flask import Flask
from tasks import TaskLogic
from blueprints.tasks import mod_tasks
from sqlalchemy import create_engine
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

app.config.from_object('config.Config')

engine = create_engine(app.config['DATABASE_URI'], echo=False)

formatter = logging.Formatter(app.config['LOG_FORMAT'])
handler = RotatingFileHandler(app.config['LOG_FILE'])
handler.setFormatter(formatter)
handler.setLevel(app.config['LOG_LEVEL'])

app.logger.addHandler(handler)

# Add application logic to flask app (?)
app.tasks = TaskLogic(db_engine=engine)
app.register_blueprint(mod_tasks, url_prefix="/tasks")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=6500, debug=True)
    except Exception:
        app.logger.exception('Failed')
