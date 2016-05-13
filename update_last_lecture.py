from google.appengine.ext import ndb
from datetime import datetime
from course_feedback import CourseLastLecture
from faculty_courses import CourseTimings
import time
import threading

current_sem='F2016'

class update_last_lecture_thread (threading.Thread):
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
	
	def run(self):
		while True:	
			date_time = datetime.now()
			course_timings_query = CourseTimings.query(CourseTimings.course_sem==current_sem)
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
							last_lecture=CourseLastLecture.query(CourseLastLecture.course==course_timing.course_id)
							course_last_lecture=last_lecture.fetch()
							for course_last in course_last_lecture:
								course_last.key.delete()
							last=CourseLastLecture()
							last.course=course_timing.course_id
							last.datetime=date_time
							last.put()
							
			time.sleep(2)