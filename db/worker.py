#!/usr/bin/env python

import json
from db.dbmgr import DbMgr
from mq.amqp import Amqp

class Worker(object):
      def __init__(self, queue_name = 'database'):
          self.dbmgr = DbMgr()
	  self.amqp = Amqp(queue_name, ['front_end'])
	  self.amqp.receive(self)
 
      def __call__(self, ch, method, properties, body):
	  body = json.loads(body)
	  result = getattr(self.dbmgr, body['request'])(body)
	  if result != None:
	    result = json.dumps(result)
	    self.amqp.send('web_frontend', result)
	  ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
   print "Database worker launched."
   Worker()
