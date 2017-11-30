
from flask import Flask
# from flaskLambda import Flask
webapp = Flask(__name__)
# webapp.secret_key = 'secret_key'
webapp.config['SECRET_KEY'] = 'secretkey'
webapp.config['my_email'] = 'wangjluestc@gmail.com'

from app import main
from app import sign_up
from app import login



