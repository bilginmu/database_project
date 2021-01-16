from flask import Flask
import databaseutils as dbutils
from flask_login import LoginManager
import views

lm = LoginManager()
@lm.user_loader
def load_user(user_id):
    return dbutils.get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"
    app.add_url_rule("/", view_func=views.home_page,methods=['GET','POST'])
    app.add_url_rule("/newdrone",view_func=views.new_drone,methods=['GET','POST'])
    app.add_url_rule("/comparison",view_func=views.comparison_drone,methods=['GET','POST'])
    app.add_url_rule("/registration",view_func=views.registration,methods=['GET','POST'])
    app.add_url_rule("/basket",view_func=views.basket,methods=['GET','POST'])
    app.add_url_rule("/login",view_func=views.login_page,methods=['GET','POST'])
    app.add_url_rule("/logout",view_func=views.logout,methods=['GET','POST'])
    lm.init_app(app)
    lm.login_view = "login_page"
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
