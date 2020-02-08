import json
from flask import Blueprint, render_template, abort, redirect, url_for, request
from receipts_storage.forms import ReceiptForm, ProductForm
from receipts_storage.models import Image, Product, Receipt, Store, Tag
from receipts_storage.app import db

bp_receipt = Blueprint("receipt", __name__)

@bp_receipt.route("/receipt/new", methods=["GET", "POST"])
def new_receipt():
    form = ReceiptForm()
    if(form.validate_on_submit()):
        # Create Store if not exists
        store = Store.query.filter_by(name=form.store.data).first()
        if(not store):
            store = Store(name=form.store.data)

        # Create the Receipt
        receipt = Receipt(receipt_number=form.receipt_number.data, date=form.date.data, payed=form.date.data, store=store)

        # Add receipt tags
        if(form.tags.data != ""):
            for tag_name in json.loads(form.tags.data):
                tag = Tag.query.filter_by(name=tag_name).first()
                if(not tag):
                    tag = Tag(name=tag_name)
                receipt.tags.append(tag)

        # Save receipt images
        for img in form.images.data:
            if(img.filename):
                img = Image(image=img)
                receipt.images.append(img)
        
        # Add products
        for entry in form.products.entries:
            product = Product(name=entry.data["name"], price=entry.data["price"], returned=False)
            
            # Add product tags
            if(entry.data["tags"] != ""):
                for tag_name in json.loads(entry.data["tags"]):
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if(not tag):
                        tag = Tag(name=tag_name)
                    product.tags.append(tag)
                
            # Save product images
            for img in entry.data["images"]:
                if(img.filename):
                    img = Image(image=img)
                    product.images.append(img)

            # Add product to the receipt
            receipt.products.append(product)
        
        # Commit receipt
        db.session.add(receipt)
        db.session.commit()
        return redirect(url_for("receipt.receipt", receipt_id=receipt.id))
    return render_template("add_receipt.html", form=form)


@bp_receipt.route("/receipt/<int:receipt_id>/edit")
def edit_receipt(receipt_id):
    receipt = Receipt.query.filter_by(id=receipt_id).first()
    if(not receipt):
        abort(404)

    form = ReceiptForm()
    if(request.method == "GET"):
        form.store.data = receipt.store.name
        form.receipt_number.data = receipt.receipt_number
        form.date.data = receipt.date
        form.tags.data = ','.join([tag.name for tag in receipt.tags])

        form.products.pop_entry()
        for product in receipt.products:
            product_form = ProductForm()
            product_form.name = product.name
            product_form.price = product.price
            product_form.tags = ','.join([tag.name for tag in product.tags])

            form.products.append_entry(product_form)
        return render_template("add_receipt.html", form=form)

    # Post-request and form is validated
    elif(form.validate_on_submit()):

        # Updating store if it has been changed
        if(form.store.data != receipt.store.name):
            store = Store.query.filter_by(name=form.store.data).first()
            if(not store):
                store = Store(name=form.store.data)
            if(len(receipt.store) <= 1):
                db.session.delete(receipt.store)
            receipt.store = store
        
        # Updating receipt_number
        receipt.receipt_number = form.receipt_number.data

        # Updating date
        receipt.date = form.date.data

        # Updating tags
        if(form.tags.data == ""):
            form.tags.data = []
        old_tags = [tag.name for tag in receipt.tags]
        current_tags = json.loads(form.tags.data)
        remove_tags = [tag for tag in old_tags if tag not in current_tags]
        add_tags = [tag for tag in current_tags if tag not in old_tags]
        for tag_name in remove_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if(tag):
                receipt.tags.remove(tag)
        for tag_name in add_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if(not tag):
                tag = Tag(name=tag_name)
            receipt.tags.append(tag)
        
        # Updating products
        for entry in form.products.entries:
            pass




    

@bp_receipt.route("/receipt/<int:receipt_id>")
def receipt(receipt_id):
    receipt = Receipt.query.filter_by(id=receipt_id).first()
    if(not receipt):
        abort(404)
    return render_template("receipt.html", receipt=receipt)
