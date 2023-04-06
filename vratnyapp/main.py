import os
os.environ['KIVY_HOME'] = os.path.join(os.getcwd(), "kivy")

# db api & gui import
from dev.gui.vratny_app import VratnyApp
from dev.sqlite.db_interface import Db


#database = Db("vratnyapp\dev\sqlite\db.sqlite")
database = Db("sqlite:///vratnyapp/dev/sqlite/db.sqlite")
app = VratnyApp(database_object=database)
app.run()
