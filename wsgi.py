import os
import sys

##Virtualenv Settings
app_home = '/var/www/pys3viewerapi'
activate_this = app_home + '/pys3venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

##Replace the standard out
sys.stdout = sys.stderr

##Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

##Add this file path to sys.path in order to import app
sys.path.append('/var/www/pys3viewerapi/')

##Create appilcation for our app
from pys3viewerapi.main import app as application
