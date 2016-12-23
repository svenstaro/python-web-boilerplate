"""Schemas for the `User` model."""
from marshmallow import Schema, fields


class UserSchema(Schema):
    """User model."""

    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)

    class Meta:
        """Set strict to `True` so that `webargs` will be able to use this `Schema`."""

        strict = True
