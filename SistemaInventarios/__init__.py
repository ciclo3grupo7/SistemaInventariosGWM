from flask import Flask
import dash

serverFlask = Flask(__name__)

serverFlask.config['DE8UG'] = True

appDash = dash.Dash(__name__, server=serverFlask, url_base_pathname='/dash/')
appDash.config['suppress_callback_excepticns'] = True

from SistemaInventarios import rutas
