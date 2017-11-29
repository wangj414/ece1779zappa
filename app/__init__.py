
from flask import Flask
webapp = Flask(__name__)
webapp.secret_key = 'secret_key'

from app import main
from app import sign_up
from app import login



