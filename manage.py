from app import create_app,db
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User,Comment,Role,DriftPost
#create app instance
app = create_app('development')

#create manager instance
manager=Manager(app)
manager.add_command('server',Server)

migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict (app=app,db=db,User=User,Comment=Comment,DriftPost=DriftPost,Role=Role)

if __name__=='__main__':
    manager.run() 