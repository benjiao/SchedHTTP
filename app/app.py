#!flask/bin/python
from flask import Flask
from modules.tasks import mod_tasks

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.register_blueprint(mod_tasks, url_prefix="/tasks")

app.run(host='0.0.0.0', debug=False)
