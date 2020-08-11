"""
Registraton service
"""
import typing

from database.models import User


class RegisterService:
    """
    Register service
    """

    def __init__(self, form):
        """
        init class by puting form data
        :params form: user

        """
        self._form = form

    def add_user(self) -> typing.Optional[dict]:
        """
        Aff user data for bin

        :return: dict for session
        """

        user = User()
        user.mail = self._form.mail.data
        user.password = self._form.password.data
        user.save()

        return {
            "id": user.id,
        }

    def check_user(self) -> bool:
        """
        Check user in database

        :return: bool
        """
        user = User.query.filter_by(mail=self._form.mail.data).first()

        return bool(user)
