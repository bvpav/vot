import flask_sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


db = flask_sqlalchemy.SQLAlchemy(model_class=Base)


class Video(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
        }
