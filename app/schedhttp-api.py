#!flask/bin/python
import logging
from flask import Flask
from tasks import TaskLogic
from blueprints.tasks import mod_tasks
from sqlalchemy import create_engine
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

app.config.from_object('config.Config')

engine = create_engine(
    app.config['DATABASE_URI'],
    pool_size=20,
    max_overflow=0,
    pool_recycle=3600,  # Recycle connections every 1 hr
    echo=False)

formatter = logging.Formatter(app.config['LOG_FORMAT'])
handler = RotatingFileHandler(app.config['LOG_FILE'])
handler.setFormatter(formatter)
handler.setLevel(app.config['LOG_LEVEL'])

app.logger.addHandler(handler)

# Add application logic to flask app (?)
app.tasks = TaskLogic(db_engine=engine)
app.register_blueprint(mod_tasks, url_prefix="/tasks")


@app.route('/')
def index():
    app.logger.info("Index called!")
    return "<h1>Ping!</h1><br /><h3>Welcome to SchedHTTP</h3>"

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=6500, debug=True)
    except Exception:
        app.logger.exception('Failed')
