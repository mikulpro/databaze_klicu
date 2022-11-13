from dev.gui.gui_vratny import VratnyApp
from dev.sqlite.db_interface import Db


database = Db()
app = VratnyApp()
app.run()
