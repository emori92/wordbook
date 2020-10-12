from django.test import TestCase
from django.urls import reverse
from ..views import LoginView, SignupView, ProfileUpdateView
from ..models import User


# Viewの共通部分の正常値処理
def assert_normal_get_request(self, app_name, kwargs=None):
    # request
        if kwargs:
            url = reverse(app_name, kwargs=kwargs)
        else:
            url = reverse(app_name)
        response = self.client.get(url)
        # assert http status
        self.assertEqual(response.status_code, 200)


# TestCase
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

    # 異常値


class SignupViewTests(TestCase):
    """SignupViewのテスト"""

    # 正常値
    def test_normal_siginup_request(self):
        """SignupView: 正常値"""
        # assert get method
        assert_normal_get_request(self, 'accounts:signup')

    # 異常値


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

    # 正常値
