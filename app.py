from flask import Flask
from pghr.config import LocalDevelopmentConfig
from pghr.database import db, ma

app = None

def create_app():    
    app = Flask(__name__, template_folder = 'templates')
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()
app.app_context().push()
from pghr.controllers import *

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        # port=8080
    )