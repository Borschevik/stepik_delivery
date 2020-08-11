"""
   ORM models for sqlalchemy library
"""
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from config.extenstions import db
from database.basemodel import BaseModel

order_to_meal = db.Table(
    "order_to_meal",
    db.metadata,
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"),),
    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id", ondelete="CASCADE"),),
    db.Column("created_at", db.DateTime, default=func.now()),
    db.Column("updated_at", db.DateTime, default=func.now(), onupdate=func.now()),
)


class User(BaseModel):
    """ Model for Users """

    __tablename__ = "users"

    mail = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    orders = db.relationship("Order", passive_deletes=True)

    @property
    def password(self):
        """
        Prhobit direct password creatinon
        """
        raise AttributeError("Prohibited")

    @password.setter
    def password(self, password: str):
        """
        Set password

        :param password: password in str format
        """
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password: str) -> bool:
        """
        Vakidate passwords for user

        :param password: password in str format
        """
        return check_password_hash(self.password_hash, password)


class Meal(BaseModel):
    """
    Model for meal
    """

    __tablename__ = "meals"

    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, default=0)
    description = db.Column(db.String, default="")
    picture = db.Column(db.String)
    category_id = db.Column("category_id", db.Integer, db.ForeignKey("categories.id"),)
    category = db.relationship("Category")
    orders = db.relationship("Order", secondary=order_to_meal)


class Order(BaseModel):
    """
    User model
    """

    __tablename__ = "orders"

    total_sum = db.Column(db.Integer, default=0)
    status = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"),)
    meals = db.relationship("Meal", secondary=order_to_meal)


class Category(BaseModel):
    """
    Category model
    """

    __tablename__ = "categories"

    title = db.Column(db.String)
    meals = db.relationship("Meal", passive_deletes=True)
