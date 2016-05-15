import cgi
import urllib
import os
from google.appengine.ext import ndb
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class CourseSchedule(ndb.Model):
	course = ndb.StringProperty(indexed=True)
	startDate = ndb.DateTimeProperty()
	endDate = ndb.DateTimeProperty()
	schedule = ndb.StringProperty()