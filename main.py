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
class Savings(ndb.Model):
    savingType=ndb.StringProperty(required=True)
    money_being_saved=ndb.StringProperty(required=True)
    saved_amount=ndb.StringProperty(required=False)
class Income(ndb.Model):
    income = ndb.StringProperty(required=True)
class Total(ndb.Model):
    total_amount = ndb.StringProperty(required=False)
    total_wishlist_amount=ndb.StringProperty(required=False)
class Wishlist(ndb.Model):
    item_name = ndb.StringProperty(repeated=True)
    item_price = ndb.StringProperty(repeated=True)
class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    # user_id = ndb.StringProperty(required = True)
    user_budget = ndb.KeyProperty(Budget, repeated=True)
    user_income = ndb.KeyProperty(Income, repeated=False)
    user_wishlist = ndb.KeyProperty(Wishlist, repeated=False, required=False)


class MainPage(webapp2.RequestHandler):
    def get(self):
        # comment_list = Comment.query().fetch()
        user = users.get_current_user()
        maintemp = the_jinja_env.get_template("templates/index.html")
        if user:
            email_address = user.nickname()
            self.response.write("You're logged in!")

            logout_link_html = (users.create_logout_url('/'))
            logout_html_element = {
            'logout_link_html': logout_link_html,
            'logInCheck': "loggedIn",
            }
            self.response.write(maintemp.render(logout_html_element))
        else:
            self.response.write("You're not logged in - please do so.")
            login_url = users.create_login_url('/')
            login_html_element = {
            'login_url': login_url,
            'logInCheck': "loggedOut"
            }
            self.response.write(maintemp.render(login_html_element))

class ExpensePage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to input monthly income and expenses
        expense_template = the_jinja_env.get_template("templates/expenses.html")
        user = users.get_current_user()
        email_address = user.nickname()
        nameGenerator = {
        'email_address': email_address,
        }
        self.response.write(expense_template.render(nameGenerator))

class BudgetPage(webapp2.RequestHandler):
    def get(self):
        budget_template = the_jinja_env.get_template("templates/budget.html")

        budget_all=Budget.query().fetch()
        income_all=Income.query().fetch()
        total_all=Total.query().fetch()
        saving_all=Savings.query().fetch()
        # wishlist_list=Wishlist.query().fetch()
        self.response.write(budget_template.render({'budget_info': budget_all,
                                                    'income_info':income_all[0],
                                                    'total_info': total_all[0],
                                                    'saving_info':saving_all[0],
                                                    }))


class budgetConfirmPage(webapp2.RequestHandler):
    def post(self):
        the_total=0;

        blogs_template = the_jinja_env.get_template('templates/budget_confir.html')
        the_amount= self.request.get('amount')
        the_des=self.request.get('description_of_thing')
        the_expenses=self.request.get("dropdown")
        the_income=self.request.get("income_added")
        the_counter=self.request.get("counter")
        the_saving_type=self.request.get("savings_set")
        the_money_being_saved=self.request.get("savingType")



        new_budget_entity = Budget(expenses = the_expenses,
                                   description = the_des,
                                   expense_amount = the_amount,
                                   )
        new_budget_entity.put()
        the_total+=int(the_amount)

        new_income_entity= Income(income=the_income)
        new_income_entity.put()


        if(int(the_counter)!=0):
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

        new_savings_entity= Savings(savingType=the_saving_type,
                                    money_being_saved=the_money_being_saved
                                    )
        new_savings_entity.put()







        budget_list = Budget.query().fetch()
        the_total=int(the_income)-the_total
        the_string_total=str(the_total)
        new_total_entity= Total(total_amount=the_string_total,
                                total_wishlist_amount='40')
        new_total_entity.put()

        if(new_savings_entity.savingType=="savingPerMonth"):
            the_total+=int(new_savings_entity.money_being_saved)
        else:
            rec=int(new_income_entity.income)*.2
            m_t_s=int(new_total_entity.total_wishlist_amount)/rec
            new_savings_entity.money_being_saved=str(m_t_s)
            new_savings_entity.put()

        self.response.write(blogs_template.render({'budget_info' : new_budget_entity,
                                                   'budget_info2': budget_list,
                                                   'income_info': new_income_entity,
                                                   'total_info': new_total_entity,
                                                   'saving_info': new_savings_entity}))
class WishAddPage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to input monthly income and expenses
        addwish_template = the_jinja_env.get_template("templates/add_wishlist.html")
        self.response.write(addwish_template.render())
class WishlistPage(webapp2.RequestHandler):
    def post(self):
        the_wishlist_total=0;

        wish_template = the_jinja_env.get_template('templates/wishlist.html')
        price = self.request.get('inserted_price')
        item_name = self.request.get('inserted_item_name')
        the_counter=self.request.get("counter")


        price_list = []
        item_list = []

        price= self.request.get('myInputs[0]')
        item_name=self.request.get('describe[0]')
        price_list.append(price)
        item_list.append(item_name)
        the_wishlist_total+=int(price)

        if(int(the_counter)!=0):
            for i in range(1,int(the_counter)+1):
                price2= self.request.get('myInputs['+str(i)+']')
                item_name2=self.request.get('describe['+str(i)+']')
                # the_expenses2=self.request.get("drop["+str(i)+"]")
                # new_budget_entity2 = Budget(expenses = the_expenses2,
                #                               description = the_des2,
                #                               expense_amount = the_amount2,
                #                               )
                price_list.append(price2)
                item_list.append(item_name2)
                # new_budget_entity2.put()
                the_wishlist_total+=int(price2)

        # new_savings_entity= Savings(savingType=the_saving_type,
        #                             money_being_saved=the_money_being_saved
        #                             )
        # new_savings_entity.put()
        # if(new_savings_entity.savingType=="savingPerMonth"):
        #         the_total+=int(new_savings_entity.money_being_saved)
        new_wishlist = Wishlist(item_name = item_list, item_price = price_list)
        new_wishlist.put()

        the_string_wishlist_total=str(the_wishlist_total)
        new_total_entity= Total(total_wishlist_amount=the_string_wishlist_total)
        new_total_entity.put()

        # budget_list = Budget.query().fetch()
        # the_total=int(the_income)-the_total
        # the_string_total=str(the_total)
        # new_total_entity= Total(total_amount=the_string_total)
        # new_total_entity.put()

        self.response.write(wish_template.render({'listofitems' : new_wishlist.item_name,
                                                  'listofprices' : new_wishlist.item_price,
                                                  'wishlist_total_info': new_total_entity
                                                   }))

class BarPage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to input monthly income and expenses
        bar_template = the_jinja_env.get_template("templates/bar.html")
        user = users.get_current_user()
        email_address = user.nickname()
        saving_all=Savings.query().fetch()
        savingM2 = int(saving_all[0].money_being_saved) * 2
        savingM6 = int(saving_all[0].money_being_saved) * 6
        savingM12 = int(saving_all[0].money_being_saved) * 12
        saving_all.append(savingM2)
        saving_all.append(savingM6)
        saving_all.append(savingM12)
        nameGenerator = {
        'email_address': email_address,
        'saving_info': saving_all[0],
        'savingM2': saving_all[1],
        'savingM6': saving_all[2],
        'savingM12': saving_all[3],
        }
        self.response.write(bar_template.render(nameGenerator))

app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/expenses", ExpensePage),
    ("/budget.html", BudgetPage),
    ("/budget_confir.html", budgetConfirmPage),
    ("/add_wishlist", WishAddPage),
    ("/wishlist.html", WishlistPage),
    ("/bar", BarPage)
], debug=True)
