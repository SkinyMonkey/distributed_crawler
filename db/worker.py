#!/usr/bin/env python

import json
from db.dbmgr import DbMgr
from mq.amqp import Amqp

class Worker(object):
      def __init__(self, queue_name = 'database'):
          self.dbmgr = DbMgr()
	  print('Worker launched on [%s]' % queue_name)
	  self.amqp = Amqp(self, queue_name)
       
      def __call__(self, ch, method, properties, body):
	  body = json.loads(body)
	  # FIXME : repartir selon la demande : ajout d'entree/fetch etc
	  ch.basic_ack(delivery_tag = method.delivery_tag)
