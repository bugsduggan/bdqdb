import os
basedir = os.path.abspath(os.path.dirname(__file__))

HOST = '127.0.0.1'
PORT = 5000
DEBUG = False

SQLALCHEMY_DATABASE_ENGINE = 'sqlite'
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_ENGINE + ':///' + os.path.join(basedir,
                                                                             'bdqdb.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
