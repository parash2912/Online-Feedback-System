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

class CourseFeedback(ndb.Model):
	course=ndb.StringProperty(indexed=True, required=True)
	sem=ndb.StringProperty(indexed=True)
	instructor_ability=ndb.IntegerProperty()
	clarity=ndb.IntegerProperty()
	blackboard=ndb.IntegerProperty()
	lecture_quality=ndb.IntegerProperty()
	prepare_degree=ndb.IntegerProperty()
	instructor_rating=ndb.IntegerProperty()
	textbook_usefulness=ndb.IntegerProperty()
	difficulty=ndb.IntegerProperty()
	coursework_amount=ndb.IntegerProperty()
	pace=ndb.IntegerProperty()
	date_time=ndb.DateTimeProperty(auto_now_add=True)

class CourseLastLecture(ndb.Model):
	course=ndb.StringProperty(indexed=True,required=True)
	datetime=ndb.DateTimeProperty()