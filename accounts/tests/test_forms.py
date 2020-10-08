from django.test import TestCase
from django.urls import reverse
from ..models import User
from ..forms import SignupForm, ProfileForm


class SignupFormTests(TestCase):
    """SignupFormのテスト"""

    # 正常値
    def test_sign_up_normal_user(self):
        """正常値: SignupForm"""
        # form
        params = {'username': 'u' * 150, 'password': 'p' * 128}
        form = SignupForm(params)
        # assert form validation
        self.assertTrue(form.is_valid())
        # response
        path = reverse('accounts:signup')
        response = self.client.post(path, params)
        # assert http status
        self.assertEqual(response.status_code, 302)

    # 異常値
    def test_sign_up_abnormal_user(self):
        """異常値: SignupForm"""
        # 異常値: username, password
        usernames = ['', 'u'*151, 'ユ'*151]
        passwords = ['', 'p'*129, 'パ'*129]
        # function: assert Form data
        def assert_form_data(usernames=['u'*150], passwords=['p'*128]):
            for name in usernames:
                for password in passwords:
                    # form
                    params = {'username': name, 'password': password}
                    form = SignupForm(params)
                    # assert validation
                    self.assertFalse(form.is_valid())
                    # response
                    path = reverse('accounts:signup')
                    response = self.client.post(path, params)
                    # assert http status
                    self.assertEqual(response.status_code, 200)  # redirect to SignUp form
        # assert
        assert_form_data(usernames=usernames)
        assert_form_data(passwords=passwords)


class ProfileFormTests(TestCase):
    """ProfileFormのテスト"""

    # create user
    def setUp(self):
        self.test_user = User.objects.create_user('test_user', password='password')

    # 正常値
    def test_profile_form_normal_user(self):
        """正常値: ProfileForm"""
        # form
        params = {'describe': 'd' * 80}
        form = ProfileForm(params)
        # assert form validation
        self.assertTrue(form.is_valid())
        # response
        path = reverse('accounts:profile', kwargs={'pk': self.test_user.id})
        # avoid LoginRequiredMixin
        self.client.login(username='test_user', password='password')
        response = self.client.post(path, params)
        # assert http status
        self.assertEqual(response.status_code, 302)

    # 異常値
    def test_profile_form_abnormal_user(self):
        """異常値: ProfileForm"""
        # 異常値: describe
        describes = ['d'*81, '説'*81]
        # assert
        for describe in describes:
            params = {'describe': describe}
            # form
            form = ProfileForm(params)
            # response
            path = reverse('accounts:profile', kwargs={'pk': self.test_user.id})
            self.client.login(username='test_user', password='password')
            response = self.client.post(path, params)
            # assert http status
            self.assertEqual(response.status_code, 200)
            # assert form validation
            self.assertFalse(form.is_valid())
