import os
os.environ['KIVY_HOME'] = os.path.join(os.getcwd(), "kivy")

# db api & gui import
from pathlib import Path
import importlib.util
main_folder_path = Path(__file__).resolve().parent
project_folder_path = main_folder_path.parent

# db_interface
module_path = os.path.join(project_folder_path, 'vratnyapp\dev\sqlite', 'db_interface.py')
spec = importlib.util.spec_from_file_location('db_interface', module_path)
module_to_import = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_to_import)
Db = module_to_import.Db

# VratnyApp
module_path = os.path.join(project_folder_path, 'vratnyapp\dev\gui', 'gui_vratny.py')
spec = importlib.util.spec_from_file_location('gui_vratny', module_path)
module_to_import = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_to_import)
VratnyApp = module_to_import.VratnyApp

#database = Db("vratnyapp\dev\sqlite\db.sqlite")
database = Db("sqlite:///dev/sqlite/db.sqlite")
app = VratnyApp(database_object=database)
app.run()