#!/usr/bin/env python

import json
from crawling.crawler import Crawler
from mq.amqp import Amqp
          
class Worker(object):
      def __init__(self, queue_name = 'crawling'):
	  self.amqp = Amqp(queue_name, ['database'])
          self.crawler = Crawler(self.amqp)
	  self.amqp.receive(self)
       
      def __call__(self, ch, method, properties, body):
	  body = json.loads(body)
	  print 'Search for tag %s to maximum depth : %s'\
	      % (body['tag'], body['max_depth'])
	  self.crawler(body['job_id'], body['urls'], body['tag'], body['max_depth'])
	  ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
   print "Crawling worker launched."
   Worker()
