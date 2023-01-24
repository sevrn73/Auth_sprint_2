from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app import start_app
import sys, os

sys.path.append(os.path.dirname(__file__))

app = start_app()

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
