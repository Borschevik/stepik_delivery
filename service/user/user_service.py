"""
Service for working with user
"""
import typing

from database.models import User


class UserService:
    """
    User servie
    """

    def __init__(self, form):
        """
        Init class by puting form data
        :params form: user

        """
        self._form = form

    def get_user(self) -> typing.Optional[dict]:
        """
        Get data for bin

        :return: dict with meals
        """
        user = User.query.filter_by(mail=self._form.mail.data).first()
        if user and user.password_valid(self._form.password.data):
            return {
                "mail": user.mail,
            }
        else:
            return None
