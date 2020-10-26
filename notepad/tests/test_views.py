"""このtest_viewsでは、Seleniumを用いてWebブラウザを中心にtestする"""


from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
# model and my module
from accounts.models import User
from notepad.models import Note
from config.my_test_module import create_user, assert_normal_get_request, assert_pagination, redirect_dashboard, login_selenium, run_selenium_js_btn


# tests
class HomeViewTests(TestCase):
    """Homeのテスト"""

    # 正常値
    def test_normal_value_home_view(self):
        """HomeView: 正常値"""
        # get request
        url = reverse('notepad:home')
        assert_normal_get_request(self, url)
        # redirect dashboard
        redirect_dashboard(self, url)


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
        # get request
        assert_normal_get_request(self, url)
        # pagination
        pagination_list = ['ranking_stars', 'ranking_users', 'ranking_tags']
        assert_pagination(self, url, pagination_list)
        # JS
        params = {
            'self': self,
            'url': url,
            'id_list': ['star', 'user', 'category'],
            'class_list': ['star-text', 'user-text', 'tag-text'],
            'text_list': ['Django', 'hoge', 'test'],
        }
        run_selenium_js_btn(**params)
        # pagination
        # assert_pagination(self, url, pagination_list, page_num=1)


class HotViewTests(LiveServerTestCase):
    """HotViewのテスト"""

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
    def test_normal_value_view(self):
        """HotView: 正常値"""
        url = reverse('notepad:hot')
        # get request
        assert_normal_get_request(self, url)
        # pagination
        # pagination_list = ['object_list', 'follow', 'recommender']
        pagination_list = ['object_list', 'recommender']
        assert_pagination(self, url, pagination_list)
        # JS: dbデータなし

        # JS: dbデータあり (未ログイン)
        params = {
            'self': self,
            'url': url,
            # 'id_list': ['wordbook', 'follow', 'recommender'],
            # 'class_list': ['card-header', 'user-text', 'tag-text'],
            # 'text_list': ['Django', 'hoge', 'test'],
            'id_list': ['wordbook', 'recommender'],
            'class_list': ['card-header', 'card-header'],
            'text_list': ['スタートアップ　…', 'Django'],
        }
        run_selenium_js_btn(**params)
        # JS: wordbookあり (ログイン)



class SearchViewTests(LiveServerTestCase):
    """SearchViewのテスト"""

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
    def test_normal_value_view(self):
        """SearchView: 正常値"""
        url = reverse('notepad:search')
        # get request
        assert_normal_get_request(self, url)
        # pagination
        pagination_list = ['wordbook', 'user', 'tag']
        assert_pagination(self, url, pagination_list)
        # JS: 検索なし
        params = {
            'self': self,
            'url': url,
            'id_list': ['wordbook', 'user', 'category'],
            'class_list': ['card-header', 'user-text', 'tag-text'],
            'text_list': ['スタートアップ　…', 'hoge', 'test'],
        }
        run_selenium_js_btn(**params)
        # JS: 検索あり


class DashboardViewTests(LiveServerTestCase):
    """DashboardViewのテスト"""

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
    def test_normal_value_view(self):
        """DashboardView: 正常値"""
        # ユーザ作成
        create_user(self, True)
        # login
        login_selenium(self)
        # get request
        url = reverse('notepad:dashboard', kwargs={'pk': self.user.pk})
        assert_normal_get_request(self, url)
        # pagination
        pagination_list = ['wordbook', 'liked']
        assert_pagination(self, url, pagination_list)
        # JS: 
        params = {
            'self': self,
            'url': url,
            'id_list': ['wordbook', 'liked'],
            'class_list': ['card-header', 'card-header'],
            'text_list': ['スタートアップ　…', 'test'],
        }
        run_selenium_js_btn(**params)


class NoteCreateViewTests(TestCase):
    """NoteCreateViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """NoteCreateView: 正常値"""
        # create user
        create_user(self)
        self.client.login(username='test_user', password='password')
        # get request
        url = reverse('notepad:note_new')
        assert_normal_get_request(self, url)
        # post request (create)


class NoteDetailViewTests(LiveServerTestCase):
    """NoteDetailViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """NoteDetailView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        wordbook_pk = Note.objects.get(user=self.user.pk).pk
        # get request
        url = reverse('notepad:note_detail', kwargs={'pk': wordbook_pk})
        assert_normal_get_request(self, url)
        # JS



class NoteUpdateViewTests(TestCase):
    """NoteUpdateViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """NoteUpdateView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # get request
        wordbook_pk = Note.objects.get(user=self.user.pk).pk
        url = reverse('notepad:note_edit', kwargs={'pk': wordbook_pk})
        assert_normal_get_request(self, url)
        # post request (update)


class NoteDeleteViewTests(TestCase):
    """NoteDeleteViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """NoteDeleteView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # get request
        wordbook_pk = Note.objects.get(user=self.user.pk).pk
        url = reverse('notepad:note_delete', kwargs={'pk': wordbook_pk})
        assert_normal_get_request(self, url)
        # delete request


class TagCreateViewTests(TestCase):
    """TagCreateViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """TagCreateView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # get request
        wordbook_pk = Note.objects.get(user=self.user.pk).pk
        url = reverse('notepad:tag_new', kwargs={'note_pk': wordbook_pk})
        assert_normal_get_request(self, url)
        # post request


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
