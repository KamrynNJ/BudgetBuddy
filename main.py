import webapp2
import jinja2
import os
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
    User_budget =  = ndb.KeyProperty(Budget, repeated=False)


class MainPage(webapp2.RequestHandler):
    def get(self):
        # comment_list = Comment.query().fetch()
        maintemp = the_jinja_env.get_template("templates/homepage.html")
        self.response.write(maintemp.render())
class ExpensePage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to input monthly income and expenses
        expense_template = the_jinja_env.get_template("templates/expenses.html")
        self.response.write(expense_template.render())

class BudgetPage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to put either how much money they
        #are willing to save per month or how many months they are willing to save.
        #In addition, the budget page will retrieve the income and expense data
        #from ExpensePage.
        Budget_list = Budget.query().fetch()
        total_expenses = self.request.get("INSERTEXPENSENAME")
        total_income = self.request.get("INSERTINCOMENAME")
        new_Budget = Budget(expenses = total_expenses, income = total_income)
        new_Budget.put()
        budget_template = the_jinja_env.get_template("templates/budget.html")
        self.response.write(budget_template.render())

    def post(self):
        #This is where the page will post the remaining money (income-expenses)
        expense_template = the_jinja_env.get_template("templates/budgetConfirm.html")
        self.response.write(expense_template.render())
    #def get(self):
        #This is where we will ask the user to put either how much money they
        #are willing to save per month or how many months they are willing to save.


class budgetConfirm(webapp2.RequestHandler):
    def post(self):
        #This page will display the perviously entered amounts and then allow for
        #a redirect to the BudgetPage with calculated results
        expense_template = the_jinja_env.get_template("templates/budgetConfirm.html")
        self.response.write(expense_template.render())


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/expenses", ExpensePage),
    ("/budget", BudgetPage),
    ("/budgetConfirm", budgetConfirmPage)

], debug=True)
