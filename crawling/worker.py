#!/usr/bin/env python

import json
from crawling.crawler import Crawler
from mq.amqp import Amqp
          
class Worker(object):
      def __init__(self, queue_name = 'crawling'):
          self.crawler = Crawler()
	  print('Worker launched on [%s]' % queue_name)
	  self.amqp = Amqp(self, queue_name)
       
      def __call__(self, ch, method, properties, body):
	  body = json.loads(body)
	  print 'Search for tag %s to maximum depth : %s' % (body['tag'], body['max_depth'])
	  self.crawler(body['urls'], body['tag'], body['max_depth'])
	  results = json.dumps(self.crawler.results)
	  print results
	  ch.basic_ack(delivery_tag = method.delivery_tag)
