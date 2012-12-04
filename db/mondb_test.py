from pymongo import MongoClient
from time import sleep

IN_PROGRESS = True
OVER = False
connection = MongoClient()
db = connection.crawling
job = db.job
jobs = {'job_id' : 41}
post = {
       'urls' : [],
       'id' : 42
     }
_id = job.insert(post)
print _id
print type(_id)
print job.find_one(_id)
post['status'] = OVER
print post
print "-" * 80
del post['_id']
job.update({'_id' : _id}, {"$set" : post})
