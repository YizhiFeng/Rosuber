import os
from models import MovieQuote
import jinja2
import webapp2
from google.appengine.ext.webapp._webapp25 import RequestHandler
from google.appengine.ext import ndb

# Jinja environment instance necessary to use Jinja templates.
def __init_jinja_env():
    jenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
        autoescape=True)
    # Example of a Jinja filter (useful for formatting data sometimes)
    #   jenv.filters["time_and_date_format"] = date_utils.time_and_date_format
    return jenv

jinja_env = __init_jinja_env()

PARENT_KEY = ndb.Key("Entity", "moviequote_root")

class MovieQuotePage(webapp2.RequestHandler):
    def get(self):
        moviequotes_query = MovieQuote.query(ancestor=PARENT_KEY).order(-MovieQuote.last_touch_date_time)
        template = jinja_env.get_template("templates/base_page.html")
        values = {"moviequotes": moviequotes_query}
        self.response.out.write(template.render(values))

class InsertQuoteAction(webapp2.RequestHandler):
    
    def post(self):
        if self.request.get("entity_key"):
            moviequote_key = ndb.Key(urlsafe=self.request.get('entity_key'))
            moviequote = moviequote_key.get()
        else:
            moviequote = MovieQuote(parent=PARENT_KEY)
        

        moviequote.quote = self.request.get("quote")
        moviequote.movie = self.request.get("movie")
        moviequote.put()
        self.redirect(self.request.referer)

class DeleteQuoteAction(webapp2.RequestHandler):
    
    def post(self):
        moviequote_key = ndb.Key(urlsafe=self.request.get('entity_key'))
        moviequote_key.delete()
        self.redirect(self.request.referer)

app = webapp2.WSGIApplication([
    ('/', MovieQuotePage),
    ('/insertquote', InsertQuoteAction),
    ("/deletequote", DeleteQuoteAction)
], debug=True)
