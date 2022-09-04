import os
import json
import ast
import datetime
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web
import tornado.wsgi
from passlib.hash import pbkdf2_sha256

from tornado import gen, web, template

class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler gonna to be used instead of RequestHandler
    """
    def write_error(self, status_code, **kwargs):
        if status_code in [403, 404, 500, 503]:
            self.write('Error %s' % status_code)
        else:
            self.write('BOOM!')

class ErrorHandler(tornado.web.ErrorHandler, BaseHandler):
    """
    Default handler gonna to be used in case of 404 error
    """
    pass

class StatusHandler(BaseHandler):
  """
  GET handler to check the status on the web service
  """
  def get(self):
    self.set_status(200)
    self.finish({'status': 'Tornado REST API Service status is ok...'})

def make_app():
    settings = dict(
        cookie_secret=str(os.urandom(45)),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "web"),
        default_handler_class=ErrorHandler,
        default_handler_args=dict(status_code=404)
    )
    return tornado.web.Application([
        (r"/status", StatusHandler),
        ], **settings)

def main():
    application = make_app()
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5001))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    print("starting tornado server..........")
    main()
