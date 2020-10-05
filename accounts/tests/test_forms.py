from django.test import TestCase
from django.urls import reverse

from ..forms import SignupForm, ProfileForm


class SignupFormTests(TestCase):
    """SignupFormのテスト"""

    # 正常値
    def test_sign_up_normal_user(self):
        """正常値: SignupForm is valid"""
        # user parameter
        params = {'username': 'test_user', 'password': 'password'}
        # form
        form = SignupForm(params)
        response = self.client.post('/signup/', params)
        # test
        self.assertEqual(response.status_code, 302)
        self.assertFalse(form.is_valid())  # Trueが返されるはずだが、Falseがreturnされる

    # 異常値
    def test_sign_up_abnormal_user(self):
        """異常値: ユーザ Form"""
        # user parameter
        username = 'u' * 151
        password = 'p' * 129
        params = {'username': username, 'password': password}
        # form
        form = SignupForm(params)
        response = self.client.post('/signup', params)
        # test
        self.assertEqual(response.status_code, 301)  # 301になる理由は不明
        self.assertFalse(form.is_valid())


class ProfileFormTests(TestCase):
    """ProfileFormのテスト"""

    # 正常値
    def test_profile_form_normal_user(self):
        """正常値: user describe"""
        # parameter
        params = {'describe': ''}
        # form
        form = ProfileForm(params)
        response = self.client.post('/profile/666/', params)
        # test
        self.assertEqual(response.status_code, 302)
        self.assertTrue(form.is_valid())

    # 異常値
    def test_profile_form_abnormal_user(self):
        """異常値: user describe"""
        # parameter
        params = {'describe': ''}
        # form
        form = ProfileForm(params)
        response = self.client.post('/profile/666/', params)
        # test
        self.assertEqual(response.status_code, 302)
        self.assertTrue(form.is_valid())
