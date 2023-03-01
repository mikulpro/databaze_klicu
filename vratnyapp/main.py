import os
os.environ['KIVY_HOME'] = os.path.join(os.getcwd(), "kivy")


from vratnyapp.dev.gui.gui_vratny import VratnyApp
from vratnyapp.dev.sqlite.db_interface import Db


database = Db("sqlite:///dev/sqlite/db.sqlite")
app = VratnyApp(database_object=database)
app.run()
