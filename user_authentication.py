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

class Users(ndb.Model):
	email=ndb.StringProperty(indexed=True, required=True)
	password=ndb.StringProperty(indexed=False, required=True)
	type=ndb.StringProperty(indexed=False)

class Auth(webapp2.RequestHandler):
	def post(self):
		user_email=self.request.get('user_email')
		user_password=self.request.get('user_password')
		login_query = Users.query(Users.email==user_email)
		users_fetched = login_query.fetch()
		if len(users_fetched) > 0:
			if users_fetched[0].email==user_email and users_fetched[0].password==user_password:
				template_values = {
					'user_email': user_email,
					'user_type': users_fetched[0].type,
					'logged': 'true'
				}

				template = JINJA_ENVIRONMENT.get_template('index.html')
				self.response.write(template.render(template_values))
			else:
				template_values = {
					'logged': 'false',
					'prev_attempt': 'true',
				}
				template = JINJA_ENVIRONMENT.get_template('login.html')
				self.response.write(template.render(template_values))
		else:
			template_values = {
				'logged': 'false',
				'prev_attempt': 'true',
			}
			template = JINJA_ENVIRONMENT.get_template('login.html')
			self.response.write(template.render(template_values))

