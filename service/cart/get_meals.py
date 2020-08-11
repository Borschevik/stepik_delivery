"""
Get meals by id
"""
import typing
from collections import defaultdict

from database.models import Meal


class GetMeals:
    """
    Get meals by id list
    """

    def __init__(self, cart: typing.List[int]):
        """
        Init class for getting meals in cart

        :params cart: list with carts

        """
        self._cart = cart

    def get_bin(self) -> dict:
        """
        Get data for bin

        :return: dict with meals
        """
        meals_data: dict = defaultdict(dict)
        for meal_id in self._cart:
            meal = Meal.query.filter(Meal.id == meal_id).first()
            if meal.title not in meals_data:
                meals_data[meal.title] = dict(
                    id=meal.id, title=meal.title, price=meal.price, count=1
                )
            else:
                meals_data[meal.title]["count"] += 1
                meals_data[meal.title]["price"] = (
                    meal.price * meals_data[meal.title]["count"]
                )
        return meals_data
