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
	
class StudentSubmitted(ndb.Model):
	email=ndb.StringProperty(indexed=True,required=True)
	course=ndb.StringProperty()