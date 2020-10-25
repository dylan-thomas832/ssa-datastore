from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from .model import db
from .run import createApp


def performMigrate():
    app = createApp('datastore.config')

    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()


if __name__ == '__main__':
    performMigrate()
