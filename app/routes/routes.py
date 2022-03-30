from app import app
from flask import render_template,redirect,request,url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from osp.classes.address import Address
from osp.classes.user import Seller,User
from datetime import datetime
now = datetime.utcnow()

app.secret_key = "secretKEY"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

'''
@login_manager.user_loader
def load_user(user_id):
    return User.objects(uid = user_id).first()

@app.route("/home")
@app.route("/")
def index():
    return render_template("public_views/index.html")

@app.route("/jinja")
def jinja():
    address = Address.objects().first()
    print(address.city)
    return render_template("public_views/jinja.html" , add = address,date = now)

@app.route("/temp")
def temp():
    return redirect("/jinja")

@app.route("/about")
def about():
    return """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>
    """

@app.route("/signup" , methods = ["GET" , "POST"])
def sign_up():

    if request.method == "POST":
        req = request.form   # a dictionary, basically
        new_seller_id = Seller.create_seller(password = req["password"] , email = req["email"] , name = req["username"] , telephone = req["telephone"] , address = Address.objects().first())
        print(new_seller_id)
        if(new_seller_id[0] == False):
            return render_template("public_views/sign_up.html" , flag = "False")

    return render_template("public_views/sign_up.html" , flag = "True")

@app.route("/profile/<username>")
def profile(username):
    return render_template("public_views/profile.html")


@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if request.files:

            print(request.files["image"])
            return redirect(request.url)

    return render_template("public_views/upload_image.html")


@app.route("/login" , methods = ["GET" , "POST"])
def login():
    return render_template("public_views/login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return redirect("/mypage")

@app.route("/mypage")
@login_required
def mypage():
    return "Important secret info"
'''
