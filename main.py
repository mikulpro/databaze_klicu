from dev.gui.gui_vratny import VratnyApp
from dev.sqlite.db_interface import Db
import logging

database = Db("sqlite:///dev/sqlite/db.sqlite")
logger = logging.getLogger("app")
app = VratnyApp(database_object=database, logger=logger)
app.run()
