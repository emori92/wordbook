"""このtest_viewsでは、Seleniumを用いてWebブラウザを中心にtestする"""


from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
# model and my module
from accounts.models import User
from notepad.models import Note, Tag, Question
from config.my_module.my_test_module import create_user, assert_normal_get_request, assert_pagination, redirect_dashboard, login_selenium, run_selenium_js_btn


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

        # JS: 未ログイン
        params1 = {
            'self': self,
            'url': url,
            'id_list': ['wordbook', 'recommender'],
            'class_list': ['card-header', 'card-header'],
            'text_list': ['スタートアップ　…', 'Django'],
        }
        run_selenium_js_btn(**params1)
        # JS: ログイン済
        login_selenium(self)
        params2 = {
            'self': self,
            'url': url,
            'id_list': ['wordbook', 'follow', 'recommender'],
            'class_list': ['card-header', 'card-header', 'card-header'],
            'text_list': ['スタートアップ　…', 'test', 'Django'],
        }
        run_selenium_js_btn(**params2)


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
        create_user(self, wordbook=True)
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
            'text_list': ['Django', 'test'],
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
        pk = self.wordbook.pk
        # get request
        url = reverse('notepad:note_detail', kwargs={'pk': pk})
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
        pk = self.wordbook.pk
        url = reverse('notepad:note_edit', kwargs={'pk': pk})
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
        pk = self.wordbook.pk
        url = reverse('notepad:note_delete', kwargs={'pk': pk})
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
        pk = self.wordbook.pk
        url = reverse('notepad:tag_new', kwargs={'note_pk': pk})
        assert_normal_get_request(self, url)
        # post request


class TagListViewTests(TestCase):
    """TagListViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """TagListView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # get request
        url = reverse('notepad:tag_list', kwargs={'word': 'test'})
        assert_normal_get_request(self, url)


class TagDeleteListViewTests(TestCase):
    """TagDeleteListViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """TagDeleteListView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # get request
        pk = self.wordbook.pk
        url = reverse('notepad:tag_delete_list', kwargs={'note_pk': pk})
        assert_normal_get_request(self, url)


class TagDeleteViewTests(TestCase):
    """TagDeleteViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """TagDeleteView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # add tag
        tag, created = Tag.objects.get_or_create(name='test_tag')
        self.wordbook.tag.add(tag)
        # get request
        pk = self.wordbook.pk
        url = reverse('notepad:tag_delete', kwargs={'note_pk': pk, 'tag': tag.name})
        assert_normal_get_request(self, url, status_code=302)
        # check redirect
        redirect_url = reverse('notepad:tag_delete_list', kwargs={'note_pk': pk})
        resp = self.client.get(url)
        self.assertRedirects(resp, redirect_url)
        # delete request


class QuestionCreateViewTests(TestCase):
    """QuestionCreateViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """QuestionCreateView: 正常値"""
        # create user and wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # get request
        pk = self.wordbook.pk
        url = reverse('notepad:question_new', kwargs={'pk': pk})
        assert_normal_get_request(self, url)
        # post request


class QuestionUpdateViewTests(TestCase):
    """QuestionUpdateViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """QuestionUpdateView: 正常値"""
        # create user, wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # question
        question = Question(question='test', answer='test', note=self.wordbook)
        question.save()
        # get request
        pk = self.wordbook.pk
        url = reverse('notepad:question_edit', kwargs={'pk': pk})
        assert_normal_get_request(self, url)
        # post request


class QuestionDeleteViewTests(TestCase):
    """QuestionDeleteViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """QuestionDeleteView: 正常値"""
        # create user, wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # question
        question = Question(question='test', answer='test', note=self.wordbook)
        question.save()
        # get request
        pk = self.wordbook.pk
        url = reverse('notepad:question_delete', kwargs={'pk': pk})
        assert_normal_get_request(self, url)
        # delete request


class QuestionReviewViewTests(TestCase):
    """QuestionReviewViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """QuestionReviewView: 正常値"""
        # create user, wordbook
        create_user(self, wordbook=True)
        self.client.login(username='test_user', password='password')
        # question
        question = Question(question='test', answer='test', note=self.wordbook)
        question.save()
        # get request
        kwargs = {
            'note_pk': self.wordbook.pk,
            'question_pk': question.pk,
            'user_pk': self.user.pk,
        }
        url = reverse('notepad:question_review', kwargs=kwargs)
        assert_normal_get_request(self, url, status_code=302)
        # check redirect
        redirect_url = reverse('notepad:note_detail', kwargs={'pk': self.wordbook.pk})
        resp = self.client.get(url)
        self.assertRedirects(resp, redirect_url)
        # register review


class FollowViewTests(TestCase):
    """FollowViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """FollowView: 正常値"""
        # create user
        create_user(self)
        follow_user = User.objects.create_user('follow_test', password='follow_test')
        self.client.login(username='test_user', password='password')
        # get request
        kwargs = {
            'following': self.user.pk,
            'followed': follow_user.pk,
        }
        url = reverse('notepad:follow', kwargs=kwargs)
        assert_normal_get_request(self, url, status_code=302)
        # check redirect
        redirect_url = reverse('notepad:dashboard', kwargs={'pk': follow_user.pk})
        resp = self.client.get(url)
        self.assertRedirects(resp, redirect_url)
        # check follow


class StarViewTests(TestCase):
    """StarViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """StarView: 正常値"""
        # create user
        create_user(self, wordbook=True)
        star_user = User.objects.create_user('follow_user', password='follow_user')
        self.client.login(username='follow_user', password='follow_user')
        # get request
        kwargs = {
            'note_pk': self.wordbook.pk,
            'user_pk': star_user.pk,
        }
        url = reverse('notepad:star', kwargs=kwargs)
        assert_normal_get_request(self, url, status_code=302)
        # check redirect
        redirect_url = reverse('notepad:note_detail', kwargs={'pk': self.wordbook.pk})
        resp = self.client.get(url)
        self.assertRedirects(resp, redirect_url)
        # check star
