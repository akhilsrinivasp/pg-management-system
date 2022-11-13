
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SECRET_KEY = None 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class LocalDevelopmentConfig(Config): 
    current_dir = os.path.abspath(os.path.dirname(__file__))       
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(current_dir, "quantifiedself.db") 
    SECRET_KEY = 'Ww2GaTsdrQYLuBmn3ABCEmZrdBe4Xj'
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@localhost/foo'
    SECRET_KEY = 'Ww2GaTsdrQYLuBmn3ABCEmZrdBe4Xj'
    DEBUG = False