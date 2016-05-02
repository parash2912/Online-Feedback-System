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
	
class CoursesTaken(ndb.Model):
	email=ndb.StringProperty(indexed=True, required=True)
	name=ndb.StringProperty()
	course_taken=ndb.StringProperty()
	course_sem=ndb.StringProperty()
	
	
class FacultyHome(webapp2.RequestHandler):
	def post(self):
		user_email = self.request.get('user_email')
		courses = CoursesTaken.query(CoursesTaken.email == user_email)
		courses_fetched = courses.fetch()
		template_values={
			'user_email': user_email,
			'courses': courses_fetched
		}
		
		template = JINJA_ENVIRONMENT.get_template('facultyHome.html')
		self.response.write(template.render(template_values))