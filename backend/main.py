from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    with app.app_context():
        pass
    return app