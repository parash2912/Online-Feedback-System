#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import urllib
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2 
import logging
from user_authentication import Auth
from user_authentication import Users
from student_courses import CoursesEnrolled
from student_courses import StudentHome
from faculty_courses import CoursesTaken
from faculty_courses import FacultyHome
from student_feedback import StudentSubmitted
from course_feedback import CourseFeedback
from faculty_courses import FacultySemCourse
from faculty_courses import CourseTimings
from faculty_courses import FacultyCourseTimings

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def load_user_pass():
	lines=list(open(os.path.join(os.path.split(__file__)[0], 'userauth.txt')))
	for line in lines:
		words = line.split("\t")
		email = words[0]
		password = words[1]
		type = words[2]
		type = type.replace("\n","")
		user_temp = Users()
		user_temp.email = email
		user_temp.password = password
		user_temp.type = type
		user_temp.put()
	
load_user_pass()

def load_student_courses():
	lines=list(open(os.path.join(os.path.split(__file__)[0], 'studentCourses.txt')))
	for line in lines:
		words = line.split("\t")
		email = words[0]
		courseList = words[1]
		student_temp = CoursesEnrolled()
		student_temp.email = email
		courseList = courseList.replace("\n","")
		courses = courseList.split(" ")
		course_index=0;
		student_temp.courses_enrolled = courseList
	
	#	for course in courses:
	#		if course != None:
	#			student_temp.courses_enrolled[course_index] = course
	#			course_index += 1
		
		student_temp.put()
	
load_student_courses()

def load_faculty_courses():
	lines=list(open(os.path.join(os.path.split(__file__)[0], 'facultyCourses.txt')))
	for line in lines:
		words = line.split("\t")
		email = words[0]
		name = words[1]
		course = words[2]
		courseSem = words[3]
		courseSem = courseSem.replace("\n","")
		faculty_temp = CoursesTaken()
		faculty_temp.email = email
		faculty_temp.name = name
		faculty_temp.course_taken = course;
		faculty_temp.course_sem = courseSem;
		
		faculty_temp.put()
		
		
load_faculty_courses()


def load_faculty_course_timings():
	lines=list(open(os.path.join(os.path.split(__file__)[0], 'facultyCourseTimings.txt')))
	for line in lines:
		words = line.split("\t")
		email = words[0]
		course_id = words[1]
		course_name = words[2]
		course_year = words[3]
		course_day = words[4]
		course_time = words[5]
		course_time = course_time.replace("\n","")
		faculty_temp = CourseTimings()
		faculty_temp.email = email
		faculty_temp.course_id = course_id
		faculty_temp.course_name = course_name
		faculty_temp.course_year = course_year
		faculty_temp.course_day = course_day
		faculty_temp.course_time = course_time
		
		faculty_temp.put()
		
		
load_faculty_course_timings()

class CreateFeedback(webapp2.RequestHandler):
	def post(self):
		user_email=self.request.get('user_email')
		course=self.request.get('course')
		template_values = {
			'user_email': user_email,
			'course': course
		}
		template = JINJA_ENVIRONMENT.get_template('feedbackForm.html')
		self.response.write(template.render(template_values))
		
class SubmitFeedback(webapp2.RequestHandler):
	def post(self):
		user_email=self.request.get('user_email')
		course=self.request.get('course')
		student_submitted = StudentSubmitted()
		student_submitted.email = user_email
		student_submitted.course = course
		student_submitted.put()
		
		courseFeedback = CourseFeedback()
		courseFeedback.course = course
		courseFeedback.instructor_ability=int(self.request.get('instructor_ability'))
		courseFeedback.clarity=int(self.request.get('clarity'))
		courseFeedback.blackboard=int(self.request.get('blackboard'))
		courseFeedback.lecture_quality=int(self.request.get('lecture_quality'))
		courseFeedback.prepare_degree=int(self.request.get('prepare_degree'))
		courseFeedback.instructor_rating=int(self.request.get('instructor_rating'))
		courseFeedback.textbook_usefulness=int(self.request.get('textbook_usefulness'))
		courseFeedback.difficulty=int(self.request.get('difficulty'))
		courseFeedback.coursework_amount=int(self.request.get('coursework_amount'))
		courseFeedback.pace=int(self.request.get('pace'))
		courseFeedback.put()
		template_values = {
			'user_email': user_email,
			'user_type': 'student'
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
		
		
class MainHandler(webapp2.RequestHandler):
    def get(self):
		#self.response.write('Hello world!')
		user=users.get_current_user()
		if user:
			url=users.create_logout_url(self.request.uri)
			url_linktext='Logout'
			user1=user
			
			template_values={
				'user': user,
				'url': url,
				'url_linktext': url_linktext
			}
			
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))
		else:
			template_values = {
				'logged': 'false',
				'prev_attempt': 'false'
			}
			
			template = JINJA_ENVIRONMENT.get_template('login.html')
			self.response.write(template.render(template_values))
			
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/login', Auth),
	('/student', StudentHome),
	('/faculty', FacultyHome),
	('/createFeedback', CreateFeedback),
	('/submitFeedback', SubmitFeedback),
	('/facultySemCourse', FacultySemCourse),
	('/facultyCourseTimings', FacultyCourseTimings)
], debug=True)
