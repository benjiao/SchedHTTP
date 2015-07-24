#!flask/bin/python
from flask import Flask
from tasks import TaskLogic
from blueprints.tasks import mod_tasks
from sqlalchemy import create_engine

app = Flask(__name__)

app.config.from_object('config.Config')

engine = create_engine(app.config['DATABASE_URI'], echo=False)

# Add application logic to flask app (?)
app.tasks = TaskLogic(db_engine=engine)

app.register_blueprint(mod_tasks, url_prefix="/tasks")

if __name__ == '__main__':
    import logging
    from logging.handlers import RotatingFileHandler

    formatter = logging.Formatter(app.config['LOG_FORMAT'])

    handler = RotatingFileHandler(app.config['LOG_FILE'])
    handler.setFormatter(formatter)
    handler.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', debug=True)
