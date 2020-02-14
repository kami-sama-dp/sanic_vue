from curd import app
from gevent import monkey
from gevent.pywsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
monkey.patch_all()


if __name__ == '__main__':
    drap = DebuggedApplication(app, evalex=True)
    http_server = WSGIServer(('127.0.0.1', 8888), drap)
    http_server.serve_forever()

    #app.run(host="127.0.0.1", port=8888, debug=True)
