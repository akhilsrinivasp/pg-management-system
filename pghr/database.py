from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

engine = None
Base = declarative_base()
db = SQLAlchemy()
ma=Marshmallow()