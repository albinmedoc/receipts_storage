import json
from flask import Blueprint, render_template, abort, redirect, url_for, request
from receipts_storage.forms import ReceiptForm, ProductForm
from receipts_storage.models import Image, Product, Receipt, Store, Tag
from receipts_storage.app import db

bp_receipt = Blueprint("receipt", __name__)

@bp_receipt.route("/receipt/new", methods=["GET", "POST"])
def create():
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
        return redirect(url_for("receipt.show", receipt_id=receipt.id))
    return render_template("add_receipt.html", form=form)


@bp_receipt.route("/receipt/<int:receipt_id>/edit", methods=["GET", "POST"])
def edit(receipt_id):
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
        return render_template("edit_receipt.html", receipt=receipt, form=form)

    # Post-request and form is validated
    elif(form.validate_on_submit()):

        # Updating store if it has been changed
        if(form.store.data != receipt.store.name):
            store = Store.query.filter_by(name=form.store.data).first()
            if(not store):
                store = Store(name=form.store.data)
            if(len(receipt.store.receipts) <= 1):
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

        # - Remove tags
        for tag_name in remove_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if(tag):
                receipt.tags.remove(tag)

        # - Add tags
        for tag_name in add_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if(not tag):
                tag = Tag(name=tag_name)
            receipt.tags.append(tag)

        
        # Updating products
        old_products = [product.name for product in receipt.products]
        current_products = [product.data["name"] for product in form.products.entries]
        remove_products = [product for product in old_products if product not in current_products]

        # - Remove products
        for product_name in remove_products:
            product = Product.query.filter_by(name=product_name, receipt=receipt).first()
            if(product):
                receipt.products.remove(product)

        # - Add and update products
        for product_entry in form.products.entries:
            product_name = product_entry.data["name"]

            # Update
            if(product_name in old_products):
                product = Product.query.filter_by(name=product_name, receipt=receipt).first()
                if(product):
                    product.price = product_entry.data["price"]

                    # Updating product tags
                    old_tags = [tag.name for tag in product.tags]
                    current_tags = json.loads(product_entry.data["tags"])
                    remove_tags = [tag for tag in old_tags if tag not in current_tags]
                    add_tags = [tag for tag in current_tags if tag not in old_tags]

                    # - Remove tags
                    for tag_name in remove_tags:
                        tag = Tag.query.filter_by(name=tag_name).first()
                        if(tag):
                            product.tags.remove(tag)

                    # - Add tags
                    for tag_name in add_tags:
                        tag = Tag.query.filter_by(name=tag_name).first()
                        if(not tag):
                            tag = Tag(name=tag_name)
                        product.tags.append(tag)

            # Add
            else:
                product = Product(name=product_entry.data["name"], price=product_entry.data["price"], returned=False)
            
                # Add product tags
                if(product_entry.data["tags"] != ""):
                    for tag_name in json.loads(product_entry.data["tags"]):
                        tag = Tag.query.filter_by(name=tag_name).first()
                        if(not tag):
                            tag = Tag(name=tag_name)
                        product.tags.append(tag)
                    
                # Save product images
                for img in product_entry.data["images"]:
                    if(img.filename):
                        img = Image(image=img)
                        product.images.append(img)

                # Add product to the receipt
                receipt.products.append(product)

        db.session.add(receipt)
        db.session.commit()
        return redirect(url_for("receipt.show", receipt_id=receipt.id))
    print(form.errors)
    return "not valid"


@bp_receipt.route("/receipt/<int:receipt_id>/delete")
def delete(receipt_id):
    receipt = Receipt.query.filter_by(id=receipt_id).first()
    if(not receipt):
        abort(404)
    db.session.delete(receipt)
    db.session.commit()
    return redirect(url_for("main.home"))
    

@bp_receipt.route("/receipt/<int:receipt_id>")
def show(receipt_id):
    receipt = Receipt.query.filter_by(id=receipt_id).first()
    if(not receipt):
        abort(404)
    return render_template("receipt.html", receipt=receipt)
