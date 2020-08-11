# pylint: disable=W0612
import re

from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField, validators
from wtforms.fields.html5 import EmailField, TelField


def password_check(form, field):
    """
    Check password
    """
    # pylint: disable=W0613
    msg = (
        "Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры"
    )
    patern1 = re.compile("[a-z]+")
    patern2 = re.compile("[A-Z]+")
    patern3 = re.compile("[0-9]+")
    if (
        not patern1.search(field.data)
        or not patern2.search(field.data)
        or not patern3.search(field.data)
    ):
        raise validators.ValidationError(msg)


def validate_cart(form, field):
    """
    If any meal present
    """
    # pylint: disable=W0613
    if not field.data:
        raise validators.ValidationError("Корзина с заказами пуста")


class CartForm(FlaskForm):
    """
    Form for booking
    """

    name = StringField(
        "Ваше имя",
        validators=[
            validators.DataRequired(message="Требуется ваше имя"),
            validators.Length(min=2, max=25, message="Имя слишком короткое"),
        ],
    )
    address = StringField(
        "Адрес", validators=[validators.DataRequired(message="Требуется ваш адрес")]
    )
    phone = TelField(
        "Ваш телефон",
        validators=[
            validators.DataRequired(message="Требуется ваш телефон"),
            validators.Length(min=6, max=25, message="Номер слишком короткий"),
        ],
    )
    mail = EmailField(
        "Электронная почта",
        validators=[
            validators.DataRequired(message="Требуется ваша почта"),
            validators.Length(min=6, max=25, message="Номер слишком короткий"),
            validators.Email(message="Некорретный адрес почты"),
        ],
    )
    cart_id = HiddenField("cart_id", validators=[validate_cart])
    cart_sum = HiddenField("cart_sum", default=0, validators=[validate_cart])


class UserForm(FlaskForm):
    """
    Form for booking
    """

    mail = TelField(
        "Электропочта",
        validators=[
            validators.DataRequired(message="Требуется ваша почта"),
            validators.Length(min=6, max=25, message="Номер слишком короткий"),
            validators.Email(),
        ],
    )
    password = PasswordField(
        "Пароль",
        validators=[
            validators.DataRequired(message="Требуется пароль"),
            validators.Length(min=5, message="Пароль должен быть не менее 5 символов"),
            password_check,
        ],
    )


class RegisterForm(FlaskForm):
    """
    Form for autherntificaton
    """

    mail = TelField(
        "Электропочта:",
        validators=[
            validators.DataRequired(message="Требуется ваша почта"),
            validators.Length(min=6, max=25, message="Номер слишком короткий"),
            validators.Email(),
        ],
    )
    password = PasswordField(
        "Пароль:",
        validators=[
            validators.DataRequired(message="Требуется пароль"),
            validators.Length(min=5, message="Пароль должен быть не менее 5 символов"),
            validators.EqualTo("confirm_password", message="Пароли не совпадают"),
            password_check,
        ],
    )
    confirm_password = PasswordField("Пароль ещё раз:")
