import os
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask


BASEDIR = os.path.abspath(os.path.dirname(__file__))

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        
        TESTING = False,
        DEBUG = True,
        SECRET_KEY = os.getenv('SECRET_KEY', default='A very terrible secret key.'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'main.sqlite')
        #SQLALCHEMY_BINDS = {

          #  'tenant': 'sqlite:///' + os.path.join(BASEDIR, 'tenant.sqlite')}
    )


    return app