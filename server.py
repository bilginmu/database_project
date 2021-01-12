from flask import Flask
import views

def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", view_func=views.home_page,methods=['GET','POST'])
    app.add_url_rule("/newdrone",view_func=views.new_drone,methods=['GET','POST'])
    app.add_url_rule("/comparison",view_func=views.comparison_drone,methods=['GET','POST'])
    app.add_url_rule("/registration",view_func=views.registration,methods=['GET','POST'])
    app.add_url_rule("/basket",view_func=views.basket,methods=['GET','POST'])
    #app.add_url_rule("/logout",view_func=views.comparison_drone)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
