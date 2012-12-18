#!/usr/bin/env python
from tornado import web, httpserver, ioloop, httpclient
import json
PORT = 8888

def start(port):
  application = VisualizationApp(port)
  http_server = httpserver.HTTPServer(application)
  http_server.listen(application.port)
  ioloop.IOLoop.instance().start()

class VisualizationApp(web.Application):
  def __init__(self, port):
    web.Application.__init__(self, [
      (r"/", RootHandler),
      (r"/analyze", AHandler),
      (r"/static/(.*)", web.StaticFileHandler, {"path":"/Users/rickygrant/Documents/Web/m_visual/static/"})
    ])
    self.port = port
    
class RootHandler(web.RequestHandler):
  def get(self):
    f = open('index.html')
    self.write(f.read())
    self.flush()
    self.finish()


class AHandler(web.RequestHandler):
  def handle_request(self, response):
    if response.error:
      print 'Error: ', response.error
    else:
      self.write(response.body)
      self.flush()
    self.finish()
  
  @web.asynchronous 
  def post(self): 
    http_client = httpclient.AsyncHTTPClient()
    print 'URL: %s' % self.get_argument('anal_loc')
    http_client.fetch(self.get_argument('anal_loc'), self.handle_request)

if __name__=='__main__':
  start(PORT)
  
