#!/usr/bin/env python

import json
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, urljoin
from urllib2 import urlopen

class Crawler(object):
      def __init__(self, amqp):
	  self.__target = None
	  self.__amqp = amqp

      def __call__(self, job_id, urls, tag, max_depth = 1):
	  """
	  Process the url list to crawl their content.
	  """
	  self.__crawl_queue = list(urls)
	  self.__tag = tag
	  self.__job_id = job_id

	  # BFS (kind of)
	  for url in self.__crawl_queue:
	    self.__max_depth = max_depth

	    if url.startswith('#')\
	      or url.startswith('mailto:'):
	      continue
  
	    # declare a new url to the database, use to have an updated progress
	    self.__amqp.send('database', json.dumps({'request' : 'new_url',
						     'job_id' : job_id,
						     'url' : url}))

	    self.__target = urlparse(url)
	    try:
	      answer = urlopen(url)
	    except Exception as url_exception:
	      print str(url_exception) + " (%s)" % url
	      continue
  
	    html_content = answer.read()
	    
	    # Analysis by beautifulSoup.
	    self.__soup = BeautifulSoup(html_content)

	    # Extract the tags attribute 'href', 'src'
	    self.__get_attributes_content(tag, ('href', 'src'),\
					  self.__new_ressource)
	    if max_depth > 0:
	      self.__max_depth -= 1
	      # Extract the links
	      self.__get_attributes_content('a', ('href', 'src'),\
					    self.__send_url)
	    answer.close()
	    
	    # declare the end of the url crawling to the database,
	    # use to have an updated progress
	    self.__amqp.send('database', json.dumps({'request' : 'end_url',
						     'job_id' : job_id,
						     'url' : url}))

      def __get_attributes_content(self, tag, attributes, to_apply):
	  """
	  Extract the designated tag attributes and apply a treatment on it if
	  the access is not denied byt the robots.txt file.
	  """
	  links = self.__soup.findAll(tag)
          for link in links:
	    for attribute in attributes:
	      if link.has_key(attribute):
		final_link = self.__real_link(link.get(attribute))
		to_apply(final_link)

      def __new_ressource(self, link):
	  self.__amqp.send('database', json.dumps({'request' : 'new_ressource',
						 'tag' : self.__tag,
						 'url' : link,
						 'job_id' : self.__job_id}))
 
      def __send_url(self, link):
	  self.__amqp.send('crawling', json.dumps({'job_id' : self.__job_id,
						   'urls' : [link],
						   'tag' : 'img',
						   'max_depth' :
						   self.__max_depth}))

      def __real_link(self, link):
	  """
	  Check if the link is malformed and correct it if needed.
	  """
	  if link.startswith("http")\
	    or link.startswith("https")\
	    or link.startswith('#'):
	    return link
	  if link.startswith('/'):
	    if urlparse(link).netloc != '':
	      return 'http://' + link.strip('/')
	    link = self.__target.scheme + '://' + self.__target.netloc + link
	  else:
	    link = urljoin(self.__target.geturl(),link)
	  return link
