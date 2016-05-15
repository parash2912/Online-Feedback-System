import cgi
import urllib
import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from course_feedback import CourseFeedback
import time
import datetime
from datetime import date
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class CoursesTaken(ndb.Model):
	email=ndb.StringProperty(indexed=True, required=True)
	name=ndb.StringProperty()
	course_taken=ndb.StringProperty()
	course_sem=ndb.StringProperty()

class CourseTimings(ndb.Model):
	email=ndb.StringProperty(indexed=True, required=True)
	course_id=ndb.StringProperty(indexed=True)
	course_name=ndb.StringProperty()
	course_year=ndb.StringProperty(indexed=True)
	course_day=ndb.StringProperty()
	course_time=ndb.StringProperty()

class FacultyHome(webapp2.RequestHandler):
	def post(self):
		user_email = self.request.get('user_email')
		course_query = CoursesTaken.query(CoursesTaken.email == user_email)
		course_fetched = course_query.fetch()
		template_values={
			'user_email': user_email,
			'courses': course_fetched
		}

		template = JINJA_ENVIRONMENT.get_template('facultyHome.html')
		self.response.write(template.render(template_values))

class FacultySemCourse(webapp2.RequestHandler):
	def post(self):
		user_email = self.request.get('user_email')
		user_sem = self.request.get('sem')

		course_query = CoursesTaken.query(CoursesTaken.email == user_email)
		course_query2 = course_query.filter(CoursesTaken.course_sem == user_sem)
		course_fetched = course_query2.fetch()

		template_values={
			'user_email': user_email,
			'courses': course_fetched
		}

		template = JINJA_ENVIRONMENT.get_template('facultySemCourse.html')
		self.response.write(template.render(template_values))


class FacultyCourseTimings(webapp2.RequestHandler):
	def post(self):
		user_email = self.request.get('user_email')
		user_course = self.request.get('course_id')
		user_sem = self.request.get('sem')

		#course_query = CourseTimings.query(CourseTimings.email == user_email,
		#				CourseTimings.course_id == user_course,
		#				CourseTimings.course_year == user_sem)
		#course_fetched = course_query.fetch()

		feedback_query=CourseFeedback.query(CourseFeedback.course==user_course,CourseFeedback.sem==user_sem)
		feedbacks = feedback_query.fetch()
		dates=[]
		for feedback in feedbacks:
			date_time=feedback.date_time
			date=date_time.strftime("%Y-%m-%d")
			if date not in dates:
				dates.append(date)
			
		template_values={
			'user_email' : user_email,
			'course_id' : user_course,
			'course_sem' : user_sem,
			'dates' : dates 
		}

		template = JINJA_ENVIRONMENT.get_template('facultyCourseTimings.html')
		self.response.write(template.render(template_values))


class FacultyFeedbackReport(webapp2.RequestHandler):
	def post(self):
		user_email = self.request.get('user_email')
		user_course = self.request.get('course_id')
		user_date = self.request.get('course_day')
		user_date = datetime.strptime(user_date, '%Y-%m-%d')
		user_date2 = datetime.combine(user_date, datetime.min.time())
		user_date3 = datetime.combine(user_date, datetime.max.time())



		course_query = CourseFeedback.query(CourseFeedback.course == user_course)
		course_query2 = course_query.filter(CourseFeedback.date_time >= user_date2)
		course_query3 = course_query2.filter(CourseFeedback.date_time <= user_date3)
		course_fetched = course_query3.fetch()

		'''
		course_query = CourseFeedback.query()
		course_fetched = course_query.fetch()
		'''

		template_values={
			'user_email' : user_email,
			'courses' : course_fetched,
			'user_date' : user_date
		}

		template = JINJA_ENVIRONMENT.get_template('facultyFeedbackReport.html')
		self.response.write(template.render(template_values))

