from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
