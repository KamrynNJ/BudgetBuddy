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
    expenses = ndb.StringProperty(required=True)
    income = ndb.StringProperty(required=False)
    description=ndb.StringProperty(required=True)
    expense_amount=ndb.IntegerProperty(required=True)
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
        #This is where we will ask the user to input monthly income and expenses
        expense_template = the_jinja_env.get_template("templates/expenses.html")
        self.response.write(expense_template.render())

class BudgetPage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to put either how much money they
        #are willing to save per month or how many months they are willing to save.
        #In addition, the budget page will retrieve the income and expense data
        #from ExpensePage.
        # Budget_list = Budget.query().fetch()
        # total_expenses = self.request.get("inserted_expense")
        # total_income = self.request.get("amount")
        # new_Budget = Budget(expenses = total_expenses, income = total_income)
        # new_Budget.put()
        budget_list = Budget.query().fetch()
        budget_template = the_jinja_env.get_template("templates/budget.html")
        self.response.write(budget_template.render({"bud_list": budget_list,}))

    def post(self):
        blogs_template = the_jinja_env.get_template('templates/budget_confir.html')
        the_amount= self.request.get('amount')
        the_des=self.request.get('description_of_thing')
        the_expenses=self.request.get("dropdown")
        the_income=self.request.get("income_added")

        new_budget_entity = Budget(expenses = the_expenses,
                                   description = the_des,
<<<<<<< HEAD
                                   expense_amount = int(the_amount)
=======
                                   expense_amount = the_amount,
                                   income=the_income
>>>>>>> 6ea1223cd4d45ee1d57654b984357d168318be3c
                                   )
        new_budget_entity.put()
        blogs_info=BlogPost.query().fetch()
        self.response.write(blogs_template.render({'budget_info' : new_budget_entity}))


        #This is where the page will post the remaining money (income-expenses)



class budgetConfirmPage(webapp2.RequestHandler):
    def post(self):
        #This page will display the perviously entered amounts and then allow for
        #a redirect to the BudgetPage with calculated results
        expense_template = the_jinja_env.get_template("templates/budgetConfirm.html")
        self.response.write(expense_template.render())


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/expenses", ExpensePage),
    ("/budget.html", BudgetPage),
    ("/budget_confir.html", BudgetPage)

], debug=True)
