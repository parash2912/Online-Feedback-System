import cgi
import urllib
import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from student_feedback import StudentSubmitted

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class CoursesEnrolled(ndb.Model):
	email=ndb.StringProperty(indexed=True, required=True)
	courses_enrolled=ndb.StringProperty()
	
class StudentHome(webapp2.RequestHandler):
	def post(self):
		user_email=self.request.get('user_email')
		course_query = CoursesEnrolled.query(CoursesEnrolled.email == user_email)
		courses_fetched = course_query.fetch()
		if len(courses_fetched) == 0:
			courses=[]
		else:
			courses = courses_fetched[0].courses_enrolled.split(" ")
		feedback_query = StudentSubmitted.query(StudentSubmitted.email == user_email)
		feedback_submitted = feedback_query.fetch()
		
		template_values={
			'user_email': user_email,
			'courses': courses,
			'feedbacks': feedback_submitted
		}
			
		template = JINJA_ENVIRONMENT.get_template('studentHome.html')
		self.response.write(template.render(template_values))