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
#
import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def render_page(self, title="",entry="",error=""):
        posts = db.GqlQuery("SELECT * FROM Blog_Post "
                         " ORDER BY created DESC"
                         " LIMIT 5")

        template = jinja_env.get_template("html_stuffs.html")
        response = template.render(title=title,entry=entry,error=error,posts=posts)
        self.response.write(response)

class Blog(Handler):
    def get(self):
        self.render_page()

    def post(self):
        title = self.request.get("title")
        entry = self.request.get("entry")

        if title and entry:
            a = Blog_Post(title=title,entry=entry)
            a.put()
            self.redirect('/blog')
        else:
            error = "Uh oh! Looks like a title or post wasn't submitted. Try again!"
            self.render_page(title,entry,error)

class Blog_Post(db.Model):
    title = db.StringProperty( required = True)
    entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


app = webapp2.WSGIApplication([
    ('/blog',Blog)
], debug=True)
