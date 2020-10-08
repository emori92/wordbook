from django.test import TestCase
from accounts.models import User


class UserModelTest(TestCase):
    """Userモデルのテスト"""
    
    # create user
    def setUp(self):
        """setUp: ユーザ作成"""
        User.objects.create_user('check_user', password='password')

    # 正常値


    # 異常値
    def test_update_abnormal_user(self):
        """異常値: username/password/describeの更新"""
        # 境界値: username/password
        name1 = 'u' * 151
        name2 = 'ゆ' * 151
        password = 'a' * 129
        describe = 'd' * 81
        # get user
        user = User.objects.get(username='check_user')
        # update user
        user.username = name1
        user.set_password(password)
        user.describe = describe
        # user test
        self.assertEqual(user.username, name1)
        user.username = name2
        self.assertEqual(user.username, name2)

        # max_lengthを超えた異常値で本来はエラーのはず
