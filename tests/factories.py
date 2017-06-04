"""Module containing all factories."""
import random

from boilerplateapp.extensions import db
from boilerplateapp.models.user import User


class UserFactory():
    """A factory with a `get` method which will return new `User`."""

    count = 0

    @staticmethod
    def get(email=None):
        """Create a new `User` and add it to the database.

        The user's email will be set to 'test<number>@example.com' where
        `<number>` is an internal counter increasing by 1 every time this method is
        called.

        The user's email can also be set manually with the `email` parameter.
        """
        UserFactory.count += 1
        if not email:
            email = "test{count}@example.com".format(count=UserFactory.count)

            # Find a unique user email.
            found_unique_email = False
            while not found_unique_email:
                count = random.randint(1, 9999)
                email = 'test{count}@example.com'.format(count=count)
                user = db.session.query(User).filter(User.email == email).first()
                if not user:
                    found_unique_email = True
        new_user = User(email, "testtest")

        db.session.add(new_user)
        db.session.commit()
        return new_user
