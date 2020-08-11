"""
Account showing all accounts
"""
from collections import defaultdict

from sqlalchemy import desc

from database.models import Meal, Order, User
from utils.util_service import get_ru_month_name


class AccountService:
    """
    Account get all orders and meals
    """

    def __init__(self, mail: str):
        """
        Initiate service user_id

        :param user_id: int
        """
        self.data: dict = defaultdict(dict)
        self._mail = mail

    def get_orders(self) -> dict:
        """
        Get orders
        """
        user_id: int = User.query.filter_by(mail=self._mail).first().id
        orders: list = Order.query.join(Order, Meal.orders).filter_by(
            user_id=user_id
        ).order_by(desc(Order.created_at)).all()
        for order in orders:
            day: int = order.created_at.day
            month: str = get_ru_month_name(order.created_at.month)
            hours: str = order.created_at.strftime("%H:%M:%S")
            key: str = f"{day} {month} {hours}"
            self.data[key] = defaultdict(dict)
            self.data[key]["dishes"] = defaultdict(dict)
            self.data[key]["total"] = order.total_sum
            for meal in order.meals:
                if meal.title in self.data[key]["dishes"]:
                    self.data[key]["dishes"][meal.title] = defaultdict(dict)
                    self.data[key]["dishes"][meal.title]["count"] += 1
                    self.data[key]["dishes"][meal.title]["sum"] += meal.price
                else:
                    self.data[key]["dishes"][meal.title]["count"] = 1
                    self.data[key]["dishes"][meal.title]["sum"] = meal.price
        return self.data
