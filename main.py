import webapp2
import jinja2
import os
from google.appengine.api import users

# from classes import Budget
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)
from google.appengine.ext import ndb

class Budget(ndb.Model):
    expenses = ndb.IntegerProperty(required=True)
    income = ndb.IntegerProperty(required=True)
class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    user_id = ndb.StringProperty(required = True)
    User_budget = ndb.KeyProperty(Budget, repeated=False)


class MainPage(webapp2.RequestHandler):
    def get(self):
        # comment_list = Comment.query().fetch()
        maintemp = the_jinja_env.get_template("templates/index.html")
        self.response.write(maintemp.render())
class ExpensePage(webapp2.RequestHandler):
    def get(self):
        expense_template = the_jinja_env.get_template("templates/expenses.html")
        self.response.write(expense_template.render())
class BudgetPage(webapp2.RequestHandler):
    def post(self):
        Budget_list = Budget.query().fetch()
        total_expenses = self.request.get("inserted_expense")
        total_income = self.request.get("inserted_income")
        new_Budget = Budget(expenses = total_expenses, income = total_income)
        new_Budget.put()
        budget_template = the_jinja_env.get_template("templates/budget.html")
        self.response.write(budget_template.render())



app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/expenses", ExpensePage),
    ("/budget", BudgetPage)

], debug=True)
