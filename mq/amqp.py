#!/usr/bin/env python

import json
from pika import *

class Amqp(object):
      def __init__(self, read_on, write_on):
	  # Get the environnment.
	  with open('/home/dotcloud/environment.json') as f:
	    env = json.load(f)
	  # Establish connection with the MQ server
	  self.__connection =\
	      BlockingConnection(\
	      ConnectionParameters(str(env['DOTCLOUD_MQSERVER_AMQP_HOST']),
				   int(env['DOTCLOUD_MQSERVER_AMQP_PORT']),
				   credentials = PlainCredentials(
				     str(env['DOTCLOUD_MQSERVER_AMQP_LOGIN']),
				     str(env['DOTCLOUD_MQSERVER_AMQP_PASSWORD']))))
	  self.__channel = self.__connection.channel()
	  self.__read_on = read_on

	  # Declare the queue on which the object will read.
	  self.__channel.queue_declare(queue = read_on)

	  # Declare the queues on which the object will write.
	  for queue in write_on:
	    self.__channel.queue_declare(queue = queue)
	  print('Worker launched reading on [%s]' % read_on)

      def receive(self, callback):
	  """
	  Receive on the read channel, passing the gived callback to the
	  basic_consume method.
	  """
	  self.__channel.basic_consume(callback, queue = self.__read_on)
	  self.__channel.start_consuming()

      def send(self, send_on, request):
	  """
	  Send on a specified channel, passing the gived callback to the
	  basic_consume method.
	  """
          self.__channel.basic_publish(exchange='',
				       routing_key = send_on,
				       body=request)

      def __del__(self):
	  self.__connection.close()
