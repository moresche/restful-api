from app.views import home_view
from flask import Flask

def create_app():
    app = Flask(__name__)

    home_view.init_app(app)

    return app