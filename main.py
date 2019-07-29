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
class BarChange(ndb.Model):
    percent2 = ndb.FloatProperty(required=True)
    percent6 = ndb.FloatProperty(required=True)
    percent12 = ndb.FloatProperty(required=True)
class Savings(ndb.Model):
    savingType=ndb.StringProperty(required=True)
    money_being_saved=ndb.StringProperty(required=True)
    saved_amount=ndb.StringProperty(required=False)
class Income(ndb.Model):
    income = ndb.StringProperty(required=True)
class Total(ndb.Model):
    total_amount = ndb.StringProperty(required=False)
class Wishlist(ndb.Model):
    item_name = ndb.StringProperty(repeated=True)
    item_price = ndb.StringProperty(repeated=True)
    the_wishlist_total_amount=ndb.StringProperty(required=True)
class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    # user_id = ndb.StringProperty(required = True)
    user_budget = ndb.KeyProperty(Budget, repeated=True)
    user_income = ndb.KeyProperty(Income, repeated=False)
    user_wishlist = ndb.KeyProperty(Wishlist, repeated=False, required=False)
    user_savings = ndb.KeyProperty(Savings, repeated=False)
    user_total = ndb.KeyProperty(Total, repeated=False)
def key_2_list(key_list) :
    real_list = []
    for key in key_list:
        real_list.append(key.get())
    return real_list

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
            is_user = User.query().filter(User.email == email_address).get()
            if is_user:
                print("user in database")
            else:
                new_user = User(email = user.nickname())
                new_user.put()
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
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.nickname()).get()
        budget_all_test = current_user.user_budget

        tasks = key_2_list(budget_all_test)
        budget_all=Budget.query().fetch()
        income_all = current_user.user_income.get()
        # income_all=Income.query().fetch()
        total_all = current_user.user_total.get()
        # total_all=Total.query().fetch()
        saving_all = current_user.user_savings.get()
        # saving_all=Savings.query().fetch()
        # wishlist_list=Wishlist.query().fetch()
        self.response.write(budget_template.render({'budget_info': tasks,
                                                    'income_info':income_all,
                                                    'total_info': total_all,
                                                    'saving_info':saving_all,
                                                    }))


class budgetConfirmPage(webapp2.RequestHandler):
    def post(self):
        the_total=0.0;

        blogs_template = the_jinja_env.get_template('templates/budget_confir.html')
        negative_template = the_jinja_env.get_template('templates/expenses.html')
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
        new_budget_entity_key = new_budget_entity.put()
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.nickname()).get()
        # new_budget_entity_key.get()
        current_user.user_budget.append(new_budget_entity_key)
        the_total+=round(float(the_amount), 2)

        new_income_entity= Income(income=the_income)
        new_income_entity_key = new_income_entity.put()
        current_user.user_income = new_income_entity_key
        current_user.put()
        # print (current_user)
        # user_income_key = current_user.user_income
        # my_income = user_income_key.get()
        # print(my_income.income)


        if(int(the_counter)!=0):
            for i in range(1,int(the_counter)+1):
                the_amount2= self.request.get('myInputs['+str(i)+']')
                the_des2=self.request.get('describe['+str(i)+']')
                the_expenses2=self.request.get("drop["+str(i)+"]")
                new_budget_entity2 = Budget(expenses = the_expenses2,
                                              description = the_des2,
                                              expense_amount = the_amount2,
                                              )
                new_budget_entity_key2 = new_budget_entity2.put()
                current_user.user_budget.append(new_budget_entity_key2)
                current_user.put()
                # print (current_user)
                the_total+=round(float(the_amount2), 2)

        new_savings_entity= Savings(savingType=the_saving_type,
                                    money_being_saved=the_money_being_saved
                                    )
        new_savings_entity_key = new_savings_entity.put()
        current_user.user_savings = new_savings_entity_key
        current_user.put()





        budget_list = key_2_list(current_user.user_budget)
        # budget_list = Budget.query().fetch()  changed from this to the line before
        wishlist_list = current_user.user_wishlist.get()
        # wishlist_list = Wishlist.query().fetch()  changed from this to the line before

        # the_total=int(the_income)-the_total
        # the_string_total=str(the_total)
        # new_total_entity= Total(total_amount=the_string_total,
        #                         total_wishlist_amount='40')
        # new_total_entity.put()

        if(new_savings_entity.savingType=="savingPerMonth"):
            the_total+=round(float(new_savings_entity.money_being_saved), 2)
        else:

            m_t_s=round(float(wishlist_list.the_wishlist_total_amount)/float(new_savings_entity.money_being_saved), 2)
            the_total+=m_t_s
            new_savings_entity.saved_amount=str(m_t_s)
            new_savings_entity_key = new_savings_entity.put()
            current_user.user_savings = new_savings_entity_key
            current_user.put()
        the_total=float((the_income))-the_total
        the_string_total=str(the_total)
        new_total_entity= Total(total_amount=the_string_total,
                                )
        new_total_entity_key = new_total_entity.put()
        current_user.user_total = new_total_entity_key
        current_user.put()

        self.response.write(blogs_template.render({'budget_info' : new_budget_entity,
                                                   'budget_info2': budget_list,
                                                   'income_info': new_income_entity,
                                                   'total_info': new_total_entity,
                                                   'saving_info': new_savings_entity,
                                                   'wishlist_info': wishlist_list}))
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



        if(int(the_counter)!=10):
            for i in range(0,int(the_counter)+1):
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
                the_wishlist_total+=float(price2)

        # new_savings_entity= Savings(savingType=the_saving_type,
        #                             money_being_saved=the_money_being_saved
        #                             )
        # new_savings_entity.put()
        # if(new_savings_entity.savingType=="savingPerMonth"):
        #         the_total+=int(new_savings_entity.money_being_saved)
        new_wishlist = Wishlist(item_name = item_list, item_price = price_list, the_wishlist_total_amount=str(the_wishlist_total))
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.nickname()).get()
        new_wishlist_key = new_wishlist.put()
        current_user.user_wishlist = new_wishlist_key
        current_user.put()
        # the_string_wishlist_total=str(the_wishlist_total)


        # budget_list = Budget.query().fetch()
        # the_total=int(the_income)-the_total
        # the_string_total=str(the_total)
        # new_total_entity= Total(total_amount=the_string_total)
        # new_total_entity.put()

        self.response.write(wish_template.render({'listofitems' : new_wishlist.item_name,
                                                  'listofprices' : new_wishlist.item_price,
                                                  'wishlist_total_info': new_wishlist.the_wishlist_total_amount
                                                   }))

class BarPage(webapp2.RequestHandler):
    def get(self):
        #This is where we will ask the user to input monthly income and expenses
        bar_template = the_jinja_env.get_template("templates/bar.html")
        user = users.get_current_user()
        current_user = User.query().filter(User.email == user.nickname()).get()
        email_address = user.nickname()
        saving_all = current_user.user_savings.get()
        # saving_all=Savings.query().fetch()
        # washlist_all=Wishlist.query().fetch()
        savingM2 = 0
        savingM6 = 0
        savingM12 = 0

        wishlist_for_info=Wishlist.query().fetch()
        if(saving_all.savingType=="savingPerMonth"):
            savingM2 = round(float(saving_all.money_being_saved) * 2, 2)
            savingM2_bar=savingM2/round(float(wishlist_for_info[0].the_wishlist_total_amount), 2)
            savingM2_bar_2=savingM2_bar*100


            savingM6 = round(float(saving_all.money_being_saved) * 6, 2)
            savingM6_bar=savingM6/round(float(wishlist_for_info[0].the_wishlist_total_amount), 2)
            savingM6_bar_2=savingM6_bar*100

            savingM12 = round(float(saving_all.money_being_saved) * 12, 2)
            savingM12_bar=savingM12/round(float(wishlist_for_info[0].the_wishlist_total_amount), 2)
            savingM12_bar_2=savingM12_bar*100
            # saving_all.append(savingM2)
            # saving_all.append(savingM6)
            # saving_all.append(savingM12)
        if(saving_all.savingType=="savingForSetMonths"):
            savingM2 = round(float(saving_all.saved_amount) * 2, 2)
            savingM6 = round(float(saving_all.saved_amount) * 6, 2)
            savingM12 = round(float(saving_all.saved_amount) * 12, 2)
            # saving_all.append(savingM2)
            # saving_all.append(savingM6)
            # saving_all.append(savingM12)
        # new_bar_entity=BarChange(percent2=savingM2_bar_2,
        #                         percent6=savingM6_bar_2,
        #                         percent12=savingM12)
        # new_bar_entity.put()
        ###savingType contains
        ###savingForSetMonths or savingPerMonth(already have this code)
        ###saved_amount is the variable that contains integers for savingForSetMonths

        nameGenerator = {
        'email_address': email_address,
        'saving_info': saving_all,
        'savingM2': savingM2,
        'savingM6': savingM6,
        'savingM12': savingM12,
        }
        self.response.write(bar_template.render(nameGenerator))

class DeletePage(webapp2.RequestHandler):
    def get(self):
        detemp = the_jinja_env.get_template("templates/delete.html")
        wish=0
        bud=0
        save=0
        ins=0
        t=0
        u=0
        bc=0
        wishlist_for_info=Wishlist.query().fetch()
        budget_for_info=Budget.query().fetch()
        saving_for_info=Savings.query().fetch()
        income_for_info=Income.query().fetch()
        total_for_info=Total.query().fetch()
        bc_for_info=BarChange.query().fetch()
        for x in wishlist_for_info:
            wishlist_for_info[wish].key.delete()
            wish=wish+1
        for x in budget_for_info:
            budget_for_info[bud].key.delete()
            bud=bud+1
        for x in saving_for_info:
            saving_for_info[save].key.delete()
            save=save+1
        for x in income_for_info:
            income_for_info[ins].key.delete()
            ins=ins+1
        for x in total_for_info:
            total_for_info[t].key.delete()
            t=t+1
        for x in bc_for_info:
            bc_for_info[bc].key.delete()
            bc=bc+1
        self.response.write(detemp.render())

app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/expenses", ExpensePage),
    ("/budget.html", BudgetPage),
    ("/budget_confir.html", budgetConfirmPage),
    ("/add_wishlist", WishAddPage),
    ("/wishlist.html", WishlistPage),
    ("/bar", BarPage),
    ("/delete", DeletePage)
], debug=True)
