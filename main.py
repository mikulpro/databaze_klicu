from dev.gui.gui_vratny import VratnyApp
from dev.sqlite.db_interface import Db

database = Db("sqlite:///dev/sqlite/db.sqlite")
app = VratnyApp(database_object=database)
app.run()
