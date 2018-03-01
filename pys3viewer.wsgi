import os
import sys
from logging import Formatter, FileHandler

APP_HOME = r"/var/www/pys3viewer"


activate_this = os.path.join("/var/www/pys3viewer/venv/flask/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, APP_HOME)
os.chdir(APP_HOME)

from pys3viewerapi.main import app

handler = FileHandler("app.log")
handler.setFormatter(Formatter("[%(asctime)s | %(levelname)s] %(message)s"))
app.logger.addHandler(handler)
application = app
