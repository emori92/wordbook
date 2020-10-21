from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
# model and my module
from accounts.models import User
from config.my_test_module import assert_normal_get_request, assert_pagination, run_selenium_js_btn


# tests
class HomeViewTests(TestCase):
    """Homeのテスト"""

    # 正常値
    def test_normal_value_home_view(self):
        """HomeView: 正常値"""
        # assert get request
        assert_normal_get_request(self, reverse('notepad:home'))


class RankingViewTests(LiveServerTestCase):
    """RankingViewのテスト"""

    # selenium
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # 正常値
    def test_normal_value_ranking_view(self):
        """RankingView: 正常値"""
        url = reverse('notepad:ranking')
        # assert get request
        assert_normal_get_request(self, url)
        # assert: DBデータがなしのpagination
        pagination_list =['ranking_stars', 'ranking_users', 'ranking_tags']
        assert_pagination(self, url, pagination_list)
        # assert JS
        params = {
            'self': self,
            'url_name': url,
            'id_list': ['star', 'user', 'category'],
            'class_list': ['text-center', 'num-font', 'text-dark'],
            'text_list': ['いいね', 'ユーザー', 'タグ'],
        }
        run_selenium_js_btn(**params)
        # assert: DBデータがありのpagination
        assert_pagination(self, url, pagination_list, page_num=1)


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass


class ViewTests(TestCase):
    """Viewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """View: 正常値"""
        pass

    # 異常値
    def test_abnormal_value_view(self):
        """ View: 異常値"""
        pass
