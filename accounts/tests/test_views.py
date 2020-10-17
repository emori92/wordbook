from django.test import TestCase
from django.urls import reverse
from ..models import User


# 共通のViewのテスト
def assert_normal_get_request(self, app_name, kwargs=None, status_code=200):
    # request
    if kwargs:
        url = reverse(app_name, kwargs=kwargs)
    else:
        url = reverse(app_name)
    response = self.client.get(url)
    # assert http status
    self.assertEqual(response.status_code, status_code)


# Tests
class LoginViewTests(TestCase):
    """LoginViewのテスト"""

    # create user
    def setUp(self):
        User.objects.create_user('test_user', password='password')

    # 正常値
    def test_normal_login_request(self):
        """LoginView: 正常値"""
        # assert get method
        assert_normal_get_request(self, 'accounts:login')


class LogoutViewTests(TestCase):
    """LogoutViewのテスト"""

    # create user
    def setUp(self):
        User.objects.create_user('test_user', password='password')

    # 正常値
    def test_logout_request(self):
        """LogoutViewのテスト"""
        # assert logout
        assert_normal_get_request(self, 'accounts:logout', status_code=302)
        # logoutで正しくリダイレクトされるか確認
        self.client.login(username='test_user', password='password')
        # assert redirect
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('notepad:home'))


class SignupViewTests(TestCase):
    """SignupViewのテスト"""

    # 正常値
    def test_normal_siginup_request(self):
        """SignupView: 正常値"""
        # assert get method
        assert_normal_get_request(self, 'accounts:signup')


class ProfileUpdateViewTests(TestCase):
    """ProfileUpdateViewのテスト"""

    # create user
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='password')

    # 正常値
    def test_normal_get_request(self):
        """ProfileUpdateView: 正常値"""
        # url variable
        kwargs = {'pk': self.user.id}
        # assert get method
        assert_normal_get_request(self, 'accounts:profile', kwargs)
