"""Tests for `models.user`."""
import pytest


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestUser:
    """Tests for `models.user.User`."""

    def test_repr(self, user_factory):
        """Test the `repr` method."""
        user = user_factory.get()
        assert repr(user)
