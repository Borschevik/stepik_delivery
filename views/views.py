"""
View layer for application
"""
import typing

from flask import Blueprint, flash, redirect, render_template, request, session

from service.account.account_service import AccountService
from service.cart.get_meals import GetMeals
from service.main.show_service import ShowService as MainService
from service.ordered.ordered_service import OrderedService
from service.register.register_service import RegisterService
from service.user.user_service import UserService
from utils.util_templates import price_sum
from views.forms import CartForm, RegisterForm, UserForm

service = Blueprint("service", __name__, template_folder="templates")


@service.route("/")
def main():
    """
    Main page
    """
    categories: dict = MainService().get()
    data: dict = GetMeals(session.get("cart")).get_bin()
    counts, cart_sum = price_sum(data)

    return render_template(
        "main.html", categories=categories, count=counts, cart_sum=cart_sum
    )


@service.route("/cart/", methods=["GET", "POST"])
def cart():
    """
    Cart page
    """
    form = CartForm()
    order: typing.Optional[list] = session.get("cart")
    form.cart_id.data = order
    data: dict = GetMeals(order).get_bin()
    counts, cart_sum = price_sum(data)
    form.cart_id.data = order
    form.cart_sum.data = cart_sum

    return render_template(
        "cart.html", form=form, data=data, count=counts, cart_sum=cart_sum
    )


@service.route("/addtocart/<int:meal_id>")
def addtocart(meal_id: int):
    """
    Adding to cart

    :param meal_id: id of meal
    """
    if session.get("cart"):
        session["cart"].append(meal_id)
    else:
        session["cart"] = [meal_id]
    session.modified = True

    return redirect("/cart/")


@service.route("/removecart/<int:meal_id>")
def removecart(meal_id: int):
    """
    Removing from cart

    :param meal_id: id of meal
    """
    session["cart"].remove(meal_id)
    session["is_delete"] = True

    return redirect("/cart/")


@service.route("/account/")
def account():
    """
    Account page
    """
    data_bin: dict = GetMeals(session.get("cart")).get_bin()
    counts, cart_sum = price_sum(data_bin)
    data: list = AccountService(session.get("user")["mail"]).get_orders()

    return render_template("account.html", data=data, count=counts, cart_sum=cart_sum)


@service.route("/login/", methods=["GET", "POST"])
def login():
    """
    Login page
    """
    form = UserForm()
    if session.get("user"):
        return redirect("/account")
    if request.method == "POST":

        if not form.validate_on_submit():
            return render_template("auth.html", form=form)

        user: dict = UserService(form).get_user()
        if user:
            session["user"] = user
            return redirect("/account/")
        form.mail.errors.append("Данная почта не зарегистрирована или неверный пароль")

    return render_template("auth.html", form=form)


@service.route("/logout/")
def logout():
    """
    Cart page
    """
    session.pop("user")
    return redirect("/login/")


@service.route("/ordered/", methods=["POST"])
def ordered():
    """
    Ordered page
    """
    form = CartForm()
    OrderedService(form).add_order(session)
    return render_template("ordered.html")


@service.route("/register/", methods=["GET", "POST"])
def register():
    """
    Register page
    """
    form = RegisterForm()
    if request.method == "POST":
        register_service: RegisterService = RegisterService(form)

        if not form.validate_on_submit():
            return render_template("register.html", form=form)

        if register_service.check_user():
            form.mail.errors.append("Пользователь с таким адресом уже существует")
            return render_template("register.html", form=form)

        session["user"] = register_service.add_user()
        flash(f"Пользователь c почтой: {form.mail.data} зарегистрирован")
        return redirect("/register/")
    return render_template("register.html", form=form)


@service.errorhandler(404)
def page_not_found(e):
    """
    Error handler
    """
    # pylint: disable=W0613
    return render_template("404.html"), 404
