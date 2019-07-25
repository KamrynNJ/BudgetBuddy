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
    description=ndb.StringProperty(required=True)
    expense_amount=ndb.StringProperty(required=True)

class Income(ndb.Model):
    income = ndb.StringProperty(required=True)
class Total(ndb.Model):
    total_amount = ndb.StringProperty(required=True)

class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    user_id = ndb.StringProperty(required = True)
    User_budget = ndb.KeyProperty(Budget, repeated=False)


class MainPage(webapp2.RequestHandler):
    def get(self):
        # comment_list = Comment.query().fetch()
        user = users.get_current_user()
        maintemp = the_jinja_env.get_template("templates/index.html")
        if user:
            # email_address = user_nickname()
            self.response.write("You're logged in!")
            logout_link_html = (users.create_logout_url('/'))
            logout_html_element = {
            'logout_link_html': logout_link_html,
            }
            self.response.write(maintemp.render(logout_html_element))
        else:
            self.response.write("You're not logged in - please do so.")
            login_url = users.create_login_url('/')
            login_html_element = {
            'login_url': login_url
            }
            self.response.write(maintemp.render(login_html_element))
        
class ExpensePage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to input monthly income and expenses
        expense_template = the_jinja_env.get_template("templates/expenses.html")
        self.response.write(expense_template.render())

class BudgetPage(webapp2.RequestHandler):
    def get(self):
        budget_template = the_jinja_env.get_template("templates/budget.html")

        budget_all=Budget.query().fetch()
        income_all=Income.query().fetch()
        total_all=Total.query().fetch()
        self.response.write(budget_template.render({'budget_info': budget_all,
                                                    'income_info':income_all[0],
                                                    'total_info': total_all[0]}))


class budgetConfirmPage(webapp2.RequestHandler):
    def post(self):
        the_total=0;

        blogs_template = the_jinja_env.get_template('templates/budget_confir.html')
        the_amount= self.request.get('amount')
        the_des=self.request.get('description_of_thing')
        the_expenses=self.request.get("dropdown")
        the_income=self.request.get("income_added")
        the_counter=self.request.get("counter")



        new_budget_entity = Budget(expenses = the_expenses,
                                   description = the_des,
                                   expense_amount = the_amount,
                                   )
        new_budget_entity.put()
        the_total+=int(the_amount)

        new_income_entity= Income(income=the_income)
        new_income_entity.put()


        if(int(the_counter)!=1):
            for i in range(1,int(the_counter)+1):
                the_amount2= self.request.get('myInputs['+str(i)+']')
                the_des2=self.request.get('describe['+str(i)+']')
                the_expenses2=self.request.get("drop["+str(i)+"]")
                new_budget_entity2 = Budget(expenses = the_expenses2,
                                              description = the_des2,
                                              expense_amount = the_amount2,
                                              )
                new_budget_entity2.put()
                the_total+=int(the_amount2)



        budget_list = Budget.query().fetch()
        the_total=int(the_income)-the_total
        the_string_total=str(the_total)
        new_total_entity= Total(total_amount=the_string_total)
        new_total_entity.put()

        self.response.write(blogs_template.render({'budget_info' : new_budget_entity,
                                                   'budget_info2': budget_list,
                                                   'income_info': new_income_entity,
                                                   'total_info': new_total_entity}))



app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/expenses", ExpensePage),
    ("/budget.html", BudgetPage),
    ("/budget_confir.html", budgetConfirmPage)

], debug=True)
