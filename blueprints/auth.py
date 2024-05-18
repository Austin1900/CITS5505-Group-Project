from flask import Blueprint,render_template, request, redirect, url_for,session
from exts import db
from .forms import RegisterForms, LoginForm
from models import UserModel

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                print("Username not found")
                return redirect(url_for("auth.login"))
            if user.password == password:
                session['user_id'] = user.id
                return redirect(url_for("index"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForms(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")