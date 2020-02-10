from flask import Blueprint, render_template, redirect, abort
from flask_login import current_user, login_user, logout_user
from receipts_storage.models import Product, Receipt, Store, Tag, User
from receipts_storage.forms import LoginForm

bp_main = Blueprint("main", __name__)

@bp_main.route("/login")
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if(not user):
            abort(401)
        login_user(user)
        return redirect(url_for("main.home"))
    return render_template("login.html", form=form)
    

@bp_main.route("/logout")
def logout():
    if(current_user.is_authenticated):
        logout_user()
    return redirect(url_for("main.home"))


@bp_main.route("/")
def home():
    recent_receipts = Receipt.query.order_by(Receipt.date.desc()).limit(15).all()
    return render_template("home.html", recent_receipts=recent_receipts)


@bp_main.route("/statistics")
def statistics():
    count_receipts = Receipt.query.count()
    count_products = Product.query.count()
    count_stores = Store.query.count()
    count_tags = Tag.query.count()

    receipts = Receipt.query.all()
    receipts_sum = 0
    for receipt in receipts:
        receipts_sum = receipts_sum + receipt.sum
    
    return render_template("statistics.html", count_receipts=count_receipts, count_products=count_products, count_stores=count_stores, receipts_sum=receipts_sum, count_tags=count_tags)
