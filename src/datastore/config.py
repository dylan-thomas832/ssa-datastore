import os

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
PORT = 5432
DATABASE_NAME = "ssa"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://@localhost:{0}/{1}".format(PORT, DATABASE_NAME)
