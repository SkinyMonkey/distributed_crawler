#!/usr/bin/env python

import pika
import json
from sys import argv

request = json.dumps({'urls' : argv[1:], 'tag' : 'img', 'max_depth' : 1})
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue = 'crawling')
channel.basic_publish(exchange='',
                      routing_key='crawling',
		      body=request)
print " [x] Asked %s : %s until depth %s" % ('img', argv[1:], 1)
connection.close()
