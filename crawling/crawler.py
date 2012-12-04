#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, urljoin
from urllib2 import urlopen
from robotparser import RobotFileParser

class Crawler(object):
      def __init__(self):
	  self.results = []
	  self.link_nbr = 0
	  self.__target = None
	  self.__robot_parser = RobotFileParser()
	  # FIXME : add two sending channels
	  # crawling
	  # database

      def __call__(self, urls, to_get, max_depth = 1):
	  """
	  Process the url list to crawl their content.
	  """
	  self.__crawl_queue = list(urls)
	  for url in self.__crawl_queue:
	    if url.startswith('#')\
	      or url.startswith('mailto:'):
	      continue
	    print 'visit : %s' % url
	    self.__target = urlparse(url)
	    self.__robot_parser.set_url(url + '/robots.txt')
	    self.__robot_parser.read()
	    try:
	      answer = urlopen(url)
	    except Exception as url_exception:
	      print str(url_exception) + " (%s)" % url
	      continue
	    self.link_nbr += 1
	    html_content = answer.read()
	    self.__soup = BeautifulSoup(html_content)
	    self.__get_attributes_content(to_get, ('href', 'src'),\
					  self.results.append)
	    if max_depth > 0:
	      self.__get_attributes_content('a', ('href', 'src'),\
					    self.__crawl_queue.append)
	      max_depth -= 1
	    answer.close()

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
		if self.__robot_parser.can_fetch("*", final_link):
		  to_apply(final_link)

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

if __name__ == '__main__':
   from pprint import pprint
   from sys import argv

   c = Crawler()
   c(argv[1:], 'img', 0)
   print ("-" * 80)
   pprint(c.results)
   print c.link_nbr
