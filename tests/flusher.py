#!/usr/bin/env python

from pika import *

class Amqp(object):
      def __init__(self, callback, queue_name = '', netloc = 'localhost'):
	  self.__connection = BlockingConnection(ConnectionParameters(netloc))
	  channel = self.__connection.channel()
	  channel.queue_declare(queue = queue_name)
	  channel.basic_consume(callback,
		                queue = queue_name)
	  channel.start_consuming()

      def __del__(self):
	  self.__connection.close()

if __name__ == '__main__':
    from time import sleep
    from sys import argv

    def handle_receiving(ch, method, properties, body):
	print " [%s]\n[%s]\n[%s]\nReceived [%r]" % (ch, method, properties, body,)
	n = 0
	while n < 0:
	  sleep(1)
	  print n
	  n += 1# FIXME : debug
	ch.basic_ack(delivery_tag = method.delivery_tag)

    Amqp(handle_receiving, 'crawling')
