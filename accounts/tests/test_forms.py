from django.test import TestCase
from django.urls import reverse

from ..forms import SignupForm, ProfileForm


class SignupFormTests(TestCase):
    
    def test_submit_normal_user(self):
        """ユーザーが作成できるか"""
        response = self.client.post(
            '/accounts/signup/',
            {'username': 'test_user', 'password': 'passw0rd'}
        )
        # http 302
        status = response.status_code
        self.assertEqual(status, 302)


    def test_submit_(self):
        """ユーザーが作成できるか"""
        pass

    def test_submit_(self):
        """ユーザーが作成できるか"""
        pass
