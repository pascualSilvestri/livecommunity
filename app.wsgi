import os
import sys

# Ruta a la raíz del proyecto Django
path = '/var/www/html/livecomunity/livecommunity'
if path not in sys.path:
    sys.path.append(path)

# Nombre del módulo que contiene el objeto 'application'
os.environ['DJANGO_SETTINGS_MODULE'] = 'livecommunity.settings'

# Carga la aplicación de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()