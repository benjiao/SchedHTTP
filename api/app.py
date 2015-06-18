#!flask/bin/python
from flask import Flask
from versions.v1_0 import api_v1_0

app = Flask(__name__)

app.register_blueprint(api_v1_0, url_prefix='/v1.0')

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True)
