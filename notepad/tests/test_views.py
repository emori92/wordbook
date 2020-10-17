from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# model and my module
from accounts.models import User
from .my_test_module import assert_normal_get_request, assert_pagination


# test browser
chrome = webdriver.Chrome()


# tests
class HomeViewTests(TestCase):
    """Homeのテスト"""

    # 正常値
    def test_normal_value_home_view(self):
        """HomeView: 正常値"""
        # assert get request
        assert_normal_get_request(self, 'notepad:home')

    # 異常値
    # def test_abnormal_value_homeview(self):
    #     """HomeView: 異常値"""
    #     pass


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
        # assert get request
        assert_normal_get_request(self, 'notepad:ranking')
        # assert JavaScript
        home = 'localhost:8000'
        test_url = f'{home}{reverse("notepad:ranking")}'
        self.selenium.get(test_url)
        # wait until rendering
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.ID, 'star')))
        # element id
        id_list = ['star', 'user', 'category']
        for id in id_list:
            btn = self.selenium.find_element_by_id(f'{id}-btn')
            btn.click()

    # 異常値
    # def test_abnormal_value_view(self):
    #     """RankingView: 異常値"""
    #     pass


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
