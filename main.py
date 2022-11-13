from dev.gui.gui_vratny import VratnyApp
from dev.sqlite.db_interface import Db

database = Db("sqlite:///db_old.sqlite")
app = VratnyApp(database_object=database)
app.run()