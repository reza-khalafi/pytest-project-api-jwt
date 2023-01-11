from django.test import SimpleTestCase
from django.urls import resolve, reverse

from user.views import GetUsers, GetUserDetail, CreateUsers, DeleteUser, Login, UpdateUser


class TestUrl(SimpleTestCase):

    def test_get_users_url_resolves(self):
        url = reverse('get-users')
        # assert resolve(url).func == GetUsers Don't use view_class after func if you don't have a class view
        assert resolve(url).func.view_class == GetUsers

    def test_get_user_detail_url_resolves(self):
        url = reverse('get-user-detail', kwargs={"pk": 1})
        assert resolve(url).func.view_class == GetUserDetail

    def test_create_url_resolves(self):
        url = reverse('create-users')
        assert resolve(url).func.view_class == CreateUsers

    def test_delete_user_url_resolves(self):
        url = reverse('delete-user', kwargs={"pk": 1})
        assert resolve(url).func.view_class == DeleteUser

    def test_login_url_resolves(self):
        url = reverse('login')
        assert resolve(url).func.view_class == Login

    def test_update_url_resolves(self):
        url = reverse('update-user')
        assert resolve(url).func.view_class == UpdateUser
