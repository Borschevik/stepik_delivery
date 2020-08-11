"""
Service to get all categories and meals
"""
import random
from collections import defaultdict

from database.models import Category, Meal


class ShowService:
    """
    Show service for meals
    """

    def __init__(self):
        """
        Init service
        """
        self.result = defaultdict(list)

    def get(self) -> dict:
        """
        Get meals in dict form

        :return: dict with cetagories
        """
        categories: list = Category.query.join(Meal).all()

        for category in categories:
            for meal in random.sample(category.meals, 3):
                self.result[category.title].append(
                    {
                        "id": meal.id,
                        "title": meal.title,
                        "description": meal.description,
                        "price": meal.price,
                        "picture": meal.picture,
                    }
                )

        return self.result
