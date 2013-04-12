import sys
sys.path.append('/home/dotcloud/current')

import wsgiref.handlers
import tornado.web
import tornado.wsgi
import json

from mq.amqp import Amqp

class PushJob(tornado.web.RequestHandler):
      def __init__(self, *args, **kw):
	  super(PushJob, self).__init__(*args, **kw)
	  self.amqp = Amqp('web_frontend', ['database', 'crawling'])

      def get(self):
	  self.write("usage :<br/>Use curl to send some post request.")

      def post(self):
	  request = json.loads(self.request.body)
	  self.amqp.send('database', json.dumps({'request' : 'new_job'}))
	  self.amqp.receive(self.__get_new_job)
	  self.amqp.send('crawling', json.dumps({'job_id' : self.__new_job_id,
						 'urls' : request['urls'],
						 'tag' : 'img',
						 'max_depth' : 1}))
	  self.set_header("Content-Type", "application/json")
	  self.write(json.dumps({'job_id' : self.__new_job_id}))
      
      def __get_new_job(self, ch, method, properties, body):
	  result = json.loads(body)
	  self.__new_job_id = result['job_id']
	  ch.basic_ack(delivery_tag = method.delivery_tag)
	  ch.stop_consuming()

class GetJobStatus(tornado.web.RequestHandler):
      def __init__(self, *args, **kw):
	  super(GetJobStatus, self).__init__(*args, **kw)
	  self.amqp = Amqp('web_frontend', ['database'])

      def get(self, job_id):
	  print "Get status of [%s]" % job_id
	  self.amqp.send('database', json.dumps({'request' : 'status',
						 'job_id' : job_id}))
	  self.amqp.receive(self.__get_status)
	  self.set_header("Content-Type", "application/json")
	  self.write(self.__answer)

      def __get_status(self, ch, method, properties, body):
	  self.__answer = body
	  ch.basic_ack(delivery_tag = method.delivery_tag)
	  ch.stop_consuming()

class GetJobResult(tornado.web.RequestHandler):
      def __init__(self, *args, **kw):
	  super(GetJobResult, self).__init__(*args, **kw)
	  self.amqp = Amqp('web_frontend', ['database'])

      def get(self, job_id):
	  print "Get result of [%s]" % job_id
	  self.amqp.send('database', json.dumps({'request' : 'result',
						 'job_id' : job_id}))
	  self.amqp.receive(self.__get_results)
	  self.set_header("Content-Type", "application/json")
	  self.write(self.__answer)

      def __get_results(self, ch, method, properties, body):
	  self.__answer = body
	  ch.basic_ack(delivery_tag = method.delivery_tag)
	  ch.stop_consuming()

web_frontend = tornado.wsgi.WSGIApplication([(r"/", PushJob),
					    (r"/status/([0-9]+)", GetJobStatus),
					    (r"/result/([0-9]+)", GetJobResult)])

def application(environ, start_response):
    return web_frontend(environ, start_response)
