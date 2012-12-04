import tornado.web
import tornado.wsgi
import wsgiref.simple_server
import json

class PushJob(tornado.web.RequestHandler):
      def __init__(self):
          pass

      def post(self):
	  request = json.loads(self.request.body)
	  # choper l'id_job dans request
	  # balancer la requete a la db pour connaitre l'id
	  # attendre la reponse
	  # balancer les liens aux workers

class GetJobStatus(tornado.web.RequestHandler):
      def get(self, job_id):
	  print "Get status of [%s]" % job_id
	  # balancer la requete a la db
	  # attendre la reponse
	  # formater la reponse
	  # renvoyer

class GetJobResult(tornado.web.RequestHandler):
      def get(self, job_id):
	  print "Get result of [%s]" % job_id
	  # balancer la requete a la db
	  # attendre la reponse
	  # formater la reponse
	  # renvoyer

if __name__ == "__main__":
   application = tornado.wsgi.WSGIApplication([
						(r"/", PushJob),
						(r"/status/([0-9]+)", GetJobStatus),
						(r"/result/([0-9]+)", GetJobResult),
					      ])
   server = wsgiref.simple_server.make_server('', 8888, application)
   print "serving"
   server.serve_forever()
