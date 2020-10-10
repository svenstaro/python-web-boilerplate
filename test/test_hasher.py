from application.hasher import get_hash, verify
from application.storage import UserInput, UserModel


def test_has_verify():
    hash1 = get_hash(UserInput(name="user1", password="password1"))
    registered_user = UserModel(name="user1", pwhash=hash1)

    assert verify(registered_user, UserInput(name="user1", password="password1"))
    assert not verify(registered_user, UserInput(name="user1", password="password2"))
    assert not verify(registered_user, UserInput(name="user2", password="password1"))

