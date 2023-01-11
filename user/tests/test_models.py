from django.test import TestCase
from mixer.backend.django import mixer

from user.models import User


class TestUserModel(TestCase):

    def setUp(self) -> None:
        self.user1 = mixer.blend(User, first_name="Reza")

    def test_create_user(self):
        # Getting the last user
        last_user = User.objects.last()
        assert last_user.first_name == "Reza"

    def test_get_full_name(self):
        assert self.user1.get_full_name() == f"{self.user1.first_name} {self.user1.last_name}"

    def test_str(self):
        assert str(self.user1) == self.user1.username
