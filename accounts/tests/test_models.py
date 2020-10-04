from django.test import TestCase
from accounts.models import User


# user test
class UserModelTests(TestCase):
    """Userモデルのテスト"""
    
    def test_create_user(self):
        """異常値: ユーザー作成"""
        # abnormal value (username)
        char1 = ['u' for i in range(200)]
        char2 = ['ゆ' for i in range(200)]
        name1 = ''.join(char1)
        name2 = ''.join(char2)
        # password
        char3 = ['p' for i in range(200)]
        password = ''.join(char3)
        # create user
        user1 = User.objects.create_user(name1, password=password)
        user2 = User.objects.create_user(name2, password=password)
        # user test
        check1 = User.objects.get(username=name1)
        check2 = User.objects.get(username=name2)
        self.assertEqual(bool(check1), False)
        # self.assertEqual(user2, check2)
        # self.assertIs(user1, check1)
        # self.assertIs(user2, check2)
