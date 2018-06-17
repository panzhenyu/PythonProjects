from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from app import create_app, rstdb

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, rstdb)

def make_shell_context():
    return dict(app=app, db=rstdb)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0"))

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
