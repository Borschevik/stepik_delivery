"""
Service for saving orders
"""
from database.models import Meal, Order, User


class OrderedService:
    """
    Oredered service
    """

    def __init__(self, form):
        """
        Init class by puting form data
        :params form: user

        """
        self._form = form

    def add_order(self, session):
        """
        Add order todatabase
        """
        order = Order()
        user_id: int = User.query.filter_by(mail=session["user"]["mail"]).first().id
        order.total_sum = self._form.cart_sum.data
        order.status = "processing"
        order.mail = self._form.mail.data
        order.phone = self._form.phone.data
        order.address = self._form.address.data
        order.user_id = user_id
        for meal_id in session.get("cart"):
            meal = Meal.query.filter_by(id=meal_id).first()
            order.meals.append(meal)
        order.save()
