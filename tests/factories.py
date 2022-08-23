import factory

from db import db
from models import TraderModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class TraderFactory(BaseFactory):
    class Meta:
        model = TraderModel
    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    city = factory.Faker("city")
    email = factory.Faker("email")
    password = factory.Faker("password")