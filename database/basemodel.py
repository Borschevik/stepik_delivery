"""
Base model with attributes for other models
"""
from typing import Any, Dict

from sqlalchemy import func

from config.extenstions import db


class BaseModel(db.Model):
    """
    Based model class
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column("created_at", db.DateTime, default=func.now())
    updated_at = db.Column(
        "updated_at", db.DateTime, default=func.now(), onupdate=func.now()
    )

    @classmethod
    def create(cls, **kwargs):
        """
        Create entry in database
        """
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def _getattribute(cls, attr: str):
        """
        Gett attribute
        :param attr str: return attribute by string
        """
        return cls.__getattribute__(cls, attr)

    def save(self):
        """
        Save entry in db
        """
        self.add()
        db.session.commit()
        return self

    def add(self):
        """
        Add to session
        """
        db.session.add(self)
        return self

    def _repr(self, **fields: Dict[str, Any]) -> str:
        """
        String repr
        :fields: dict with models field

        :return: str
        """
        field_provided = []
        for column, value in fields.items():
            field_provided.append(f"{column}={value!r}")

        if field_provided:
            return f"<{self.__class__.__name__}({','.join(field_provided)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self) -> str:
        """
        Invoke string representations

        :return: string
        """
        return self._repr(id=self.id)
