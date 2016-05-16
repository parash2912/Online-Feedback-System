import cgi
import urllib
import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from datetime import datetime
from student_feedback import StudentSubmitted
from course_feedback import CourseLastLecture
from faculty_courses import CourseTimings
import time
import threading

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

current_sem='F2016'

weekdays=dict()
weekdays[0]='Monday'
weekdays[1]='Tuesday'
weekdays[2]='Wednesday'
weekdays[3]='Thursday'
weekdays[4]='Friday'
weekdays[5]='Saturday'
weekdays[6]='Sunday'



class delete_feedback_submission_thread (threading.Thread):
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID

	def run(self):
		while True:
			date_time = datetime.now()
			student_submitted_query=StudentSubmitted.query()
			student_submitted=student_submitted_query.fetch()

			for stud_sub in student_submitted:

				stud_course = stud_sub.course
				course_timings_query = CourseTimings.query(CourseTimings.course_id==stud_course,CourseTimings.course_year==current_sem)
				course_timings = course_timings_query.fetch()

				if len(course_timings) > 0:
					for course_timing in course_timings:
						str_weekday = date_time.strftime('%A')

						if str_weekday==course_timing.course_day:
							course_time=course_timing.course_time.split("-")
							course_end_time=course_time[1]
							course_end_time_spl=course_end_time.split(":")
							end_hour=date_time.strftime('%H')
							end_minute=date_time.strftime('%M')
							end_second=date_time.strftime('%S')
							if (int(end_hour)==int(course_end_time_spl[0])) and (int(end_minute)==int(course_end_time_spl[1])) and (int(end_second)>=int(course_end_time_spl[2]) and int(end_second) <= int(course_end_time_spl[2])+10):
								stud_sub.key.delete()

			time.sleep(2)