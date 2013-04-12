#!/usr/bin/env python

import json
from pymongo import MongoClient
from bson import ObjectId

class DbMgr(object):
      def __init__(self):
	  with open('/home/dotcloud/environment.json') as f:
	    env = json.load(f)
	  
	  # Connect to the Database
	  self.__connection = MongoClient('mongodb://%s:%s@%s:%s'%
					  (str(env['DOTCLOUD_DATA_MONGODB_LOGIN'])
					  ,str(env['DOTCLOUD_DATA_MONGODB_PASSWORD'])
					  ,str(env['DOTCLOUD_DATA_MONGODB_HOST'])
					  ,int(env['DOTCLOUD_DATA_MONGODB_PORT'])))
	  # The collection will be called crawling.
	  self.__db = self.__connection.crawling
	  # The collection will be called jobs.
	  self.__jobs = self.__db.jobs

      def __del__(self):
	  self.__connection.close()

      def new_job(self, request):
	  """
	  Insert a new job entry into the db.
	  """
	  nid = self.__jobs.find().count()
	  _id = self.__jobs.insert({'progress' : 0,
				    'completed' : 0,
				    'result' : [],
				    'nid': unicode(nid)})
	  return {'job_id' : unicode(nid)}

      def new_url(self, request):
	  """
	  Increment the url count for the designated job.
	  """
	  print 'New url : %s for job #%s' % (request['url'], request['job_id'])
	  self.__jobs.update({ 'nid' :  request['job_id']},\
	  		     { '$inc': { 'progress' : 1 } } )

      def end_url(self, request):
	  """
	  Decrement the count of in progress url for the designated job.
	  Increment the count of completed url for the designated job.
	  """
	  print 'End url : %s for job #%s' % (request['url'], request['job_id'])
	  self.__jobs.update({ 'nid' :  request['job_id']},\
	  		     { '$inc': { 'progress': -1 } })

	  self.__jobs.update({ 'nid' :  request['job_id']},\
	  		     { '$inc': { 'completed': 1 } })

      def new_ressource(self, request):
          """
	  Add a ressource to the current job document.
	  """
	  print 'Ressource [%s] for job [%s]' % (request['url'], request['job_id'])
	  self.__jobs.update({ 'nid' :  request['job_id']},\
			     { '$push':  { 'result' : {'tag' : request['tag'],
						       'url' : request['url']}}})

      def status(self, request):
	  try:
	    state = self.__jobs.find_one({'nid' : request['job_id']})
	    if state['progress'] == 0:
	      return
	      {
		'status' : 'over',\
		'completed' : state['completed']
	      }
	    return\
	      {
		'status' : 'in progress',\
		'completed' : state['completed'],\
		'inprogress' : state['progress'],\
	      }
	  except:
	    return {'error'  : 'this job id doesn\'t exist',
		    'job_id' : request['job_id']}

      def result(self, request):
	  try:
	    state = self.__jobs.find_one({'nid' : request['job_id']})
	    return {'result' : state['result']}
	  except:
	    return {'error'  : 'this job id doesn\'t exist',
		    'job_id' : request['job_id']}
