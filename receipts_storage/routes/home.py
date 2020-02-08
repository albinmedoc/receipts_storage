from flask import Blueprint, render_template
from receipts_storage.models import Product, Receipt, Store

bp_home = Blueprint("home", __name__)

@bp_home.route("/")
def home():
    recent_receipts = Receipt.query.order_by(Receipt.date.desc()).limit(15).all()
    return render_template("home.html", recent_receipts=recent_receipts)


@bp_home.route("/statistics")
def statistics():
    count_receipts = Receipt.query.count()
    count_products = Product.query.count()
    count_stores = Store.query.count()

    receipts = Receipt.query.all()
    receipts_sum = 0
    for receipt in receipts:
        receipts_sum = receipts_sum + receipt.sum
    
    return render_template("statistics.html", count_receipts=count_receipts, count_products=count_products, count_stores=count_stores, receipts_sum=receipts_sum)
