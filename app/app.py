#!flask/bin/python
from flask import Flask
from tasks import TaskLogic
from modules.tasks import mod_tasks
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///db/test.db', echo=False)

# Add application logic to flask app (?)
app.tasks = TaskLogic(db_engine=engine)

app.register_blueprint(mod_tasks, url_prefix="/tasks")

if __name__ == '__main__':
    import logging
    from logging.handlers import RotatingFileHandler

    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

    handler = RotatingFileHandler('foo.log')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', debug=True)
