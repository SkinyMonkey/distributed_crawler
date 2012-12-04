#!/usr/bin/env python

from pymongo import MongoClient

class DbMgr(object):
      def __init__(self, hostname, port):
	  self._id = 0
	  self.db = {}

      def new_job(self, request):
	  """
	  Insert a new job entry into the db.
	  """
	  self._id += 1
	  self.db[self._id] = {}
	  return json.dumps({'job_id' : self._id})

      def new_url(self, request):
	  """
	  Increment the url count for the designated job.
	  """
	  request = json.loads(request)
	  print 'New url : %s for job #%s' % (request['url'], request['job_id'])
	  if not self.db[request]['job_id'].has_key('progress'):
	    self.db[request['job_id']]['progress'] = 0
	    return # the count will fall to -1 when all url will be consumed
	  self.db[request['job_id']]['progress'] += 1

      def end_url(self):
	  """
	  Decrement the url count for the designated job.
	  """
	  request = json.loads(request)
	  print 'End url : %s for job #%s' % (request['url'], request['job_id'])
	  self.db[request['job_id']]['progress'] -= 1
	  if not self.db[request]['job_id'].has_key('completed'):
	    self.db[request['job_id']]['completed'] = 0
	  self.db[request['job_id']]['completed'] += 1

      def new_ressource(self, request):
          """
	  Add a ressource to the current job document.
	  """
	  request = json.loads(request)
	  if not self.db[request]['job_id'].has_key('result'):
	    self.db[request['job_id']]['result'] = []
	  self.db[request['job_id']]['result'].append(\
	      {
		'tag' : request['tag'],
		'url' : request['url']
	      })
	  return json.dumps({})

      def status(self, request):
	  request = json_loads(request)
	  try:
	    if self.db[request['job_id']]['progress'] == -1:
	      return json.dumps(
	      {
		'status' : 'over',\
		'completed' : self.db[request['job_id']]['completed']
	      })
	    return json.dumps(
	      {
		'status' : 'in progress',\
		'completed' : self.db[request['job_id']]['completed'],\
		'inprogress' : self.db[request['job_id']]['progress'],\
	      })
	  except:
	    return json.dumps({'error'  : 'this job id doesn\'t exist',
			       'job_id' : request['job_id']})

      def result(self, request):
	  # FIXME : Or it can be a json object with the list URL associated with
	  # the domain crawled, anyway works, no specific requirement here.
	  request = json_loads(request)
	  try:
	    return json.dumps({'result' : self.db[request['job_id']]['result']})
	  except:
	    return json.dumps({'error'  : 'this job id doesn\'t exist',
			       'job_id' : request['job_id']})
