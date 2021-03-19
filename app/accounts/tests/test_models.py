from django.test import TestCase
from accounts.models import User


class UserModelTest(TestCase):
    """Userモデルのテスト"""
    
    # create user
    def setUp(self):
        """setUp: ユーザ作成"""
        User.objects.create_user('check_user', password='password')

    # 異常値
    def test_update_abnormal_user(self):
        """UserModel: 異常値"""
        # 境界値: username/password
        names = ['u' * 150, 'ゆ' * 150]  # 151にするとエラー発生
        passwords = ['p' * 129, 'パ' * 129]
        describes = ['d' * 81, '説' * 81]  # describeは異常値でもエラー発生せず
        # get user
        user = User.objects.get(username='check_user')
        # update name, password, describe
        for n in names:
            for p in passwords:
                for d in describes:
                    user.username = n
                    user.set_password(p)
                    user.describe = d
                    user.save()
                    # test name, describe
                    self.assertEqual(user.username, n)
                    self.assertEqual(user.describe, d)
