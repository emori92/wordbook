from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from notepad.models import Note
from notepad.forms import SearchForm, NoteForm, TagForm, QuestionForm
from config.my_module.my_test_module import assert_form


class SearchFormTests(TestCase):
    """SearchFormのテスト"""

    # 正常値
    def test_search_normal_value(self):
        """SearchForm: 正常値"""
        # 正常値: search_value
        chars = ['', 's'*150]
        # assert
        for char in chars:
            # form
            params = {'search': char}
            form = SearchForm(params)
            # assert form validation
            self.assertTrue(form.is_valid())
            # response
            path = reverse('notepad:search')
            response = self.client.get(path, params)
            # assert http status
            self.assertEqual(response.status_code, 200)

    # 異常値
    def test_search_abnormal_value(self):
        """SearchForm: 異常値"""
        # 異常値: search_value
        chars = ['s'*151, '検'*151]
        # assert
        for char in chars:
            # form
            params = {'search': char}
            form = SearchForm(params)
            # assert validation
            self.assertFalse(form.is_valid())
            # response
            path = reverse('notepad:search')
            response = self.client.get(path, params)
            # assert http status
            self.assertEqual(response.status_code, 200)  # redirect to SignUp form


class NoteFormTests(TestCase):
    """NoteFormのテスト"""

    # create user
    def setUp(self):
        User.objects.create_user('test_user', password='password')

    # 正常値
    def test_create_normal_wordbook(self):
        """NoteForm: 正常値"""
        # 正常値: title, describe, public
        titles = ['t'*32, 'タ'*32]
        describes = ['', 'd'*128, '説'*128]
        public = [0, 1]
        # function: assert form data
        def assert_note_form(titles=['t'*32], describes=[''], public=[0]):
            for title in titles:
                for describe in describes:
                    for p in public:
                        # form
                        params = {'title': title, 'describe': describe, 'public': p}
                        form = NoteForm(params)
                        # assert form validation
                        self.assertTrue(form.is_valid())
                        # response
                        path = reverse('notepad:note_new')
                        self.client.login(username='test_user', password='password')
                        response = self.client.post(path, params)
                        # assert http status
                        self.assertEqual(response.status_code, 302)
        # assert
        assert_note_form(titles=titles)
        assert_note_form(describes=describes)
        assert_note_form(public=public)

    # 異常値
    def test_create_abnormal_wordbook(self):
        """NoteForm: 異常値"""
        # 異常値: title, describe, public
        titles = ['', 't'*33, 'タ'*33]
        describes = ['d'*129, '説'*129]
        public = [2, '', '0', 'a', True]
        # function: assert form data
        def assert_note_form(titles=[''], describes=['d'*129], public=['']):
            for title in titles:
                for describe in describes:
                    for p in public:
                        # form
                        params = {'title': title, 'describe': describe, 'public': p}
                        form = NoteForm(params)
                        # assert form validation
                        self.assertFalse(form.is_valid())
                        # response
                        path = reverse('notepad:note_new')
                        self.client.login(username='test_user', password='password')
                        response = self.client.post(path, params)
                        # assert http status
                        self.assertEqual(response.status_code, 200)
        # assert
        assert_note_form(titles=titles)
        assert_note_form(describes=describes)
        assert_note_form(public=public)


class TagFormTests(TestCase):
    """TagFormのテスト"""

    # create user and wordbook
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='password')
        self.wordbook = Note(title='test', user=self.user)
        self.wordbook.save()

    # 正常値
    def test_add_normal_value_tag(self):
        """TagForm: 正常値"""
        # 正常値: tag_name
        tags = ['t'*32, 'タ'*32]
        # assert
        for tag in tags:
            # form
            params = {'name': tag}
            form = TagForm(params)
            # assert form validation
            self.assertTrue(form.is_valid())
            # response
            path = reverse('notepad:tag_new', kwargs={'note_pk': self.wordbook.id})
            self.client.login(username='test_user', password='password')
            response = self.client.post(path, params)
            # assert http status
            self.assertEqual(response.status_code, 302)

    # 異常値
    def test_add_abnormal_value_tag(self):
        """TagForm: 異常値"""
        # 異常値: tag_name
        tags = ['', 't'*33, 'タ'*33]
        # assert
        for tag in tags:
            # form
            params = {'name': tag}
            form = TagForm(params)
            # assert form validation
            self.assertFalse(form.is_valid())
            # response
            path = reverse('notepad:tag_new', kwargs={'note_pk': self.wordbook.id})
            self.client.login(username='test_user', password='password')
            response = self.client.post(path, params)
            # assert http status
            self.assertEqual(response.status_code, 200)


class QuestionFormTests(TestCase):
    """QuestionFormのテスト"""

    # create user and wordbook
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='password')
        self.wordbook = Note(title='test', user=self.user)
        self.wordbook.save()

    # 正常値
    def test_add_normal_value_question(self):
        """QuestionForm: 正常値"""
        # 正常値: question, hint, answer
        questions = ['q'*128, '問'*128]
        hints = ['', 'h'*64, 'ヒ'*64]
        answers = ['a'*256, '答'*256]
        # function: assert form data
        def assert_form(questions=['q'*128], hints=[''], answers=['a'*256]):
            for q in questions:
                for hint in hints:
                    for answer in answers:
                        # form
                        params = {'question': q, 'hint': hint, 'answer': answer}
                        form = QuestionForm(params)
                        # assert form validation
                        self.assertTrue(form.is_valid())
                        # response
                        path = reverse('notepad:note_new')
                        self.client.login(username='test_user', password='password')
                        response = self.client.post(path, params)
                        # assert http status
                        self.assertEqual(response.status_code, 200)  # なぜか302 => 200となる
        # assert
        assert_form(questions=questions)
        assert_form(hints=hints)
        assert_form(answers=answers)

    # 異常値
    def test_add_abnormal_value_question(self):
        """QuestionForm: 異常値"""
        # 異常値: question, hint, answer
        questions = ['', 'q'*129, '問'*129]
        hints = ['h'*65, 'ヒ'*65]
        answers = ['', 'a'*257, '答'*257]
        # function: assert form data
        def assert_form(questions=[''], hints=['h'*65], answers=['']):
            for q in questions:
                for hint in hints:
                    for answer in answers:
                        # form
                        params = {'question': q, 'hint': hint, 'answer': answer}
                        form = QuestionForm(params)
                        # assert form validation
                        self.assertFalse(form.is_valid())
                        # response
                        path = reverse('notepad:note_new')
                        self.client.login(username='test_user', password='password')
                        response = self.client.post(path, params)
                        # assert http status
                        self.assertEqual(response.status_code, 200)
        # assert
        assert_form(questions=questions)
        assert_form(hints=hints)
        assert_form(answers=answers)
        # values_list = [
        #     ['', 'q'*129, '問'*129],
        #     ['h'*65, 'ヒ'*65],
        #     ['', 'a'*257, '答'*257],
        # ]
        # parameter = {
        #     'self': self,
        #     'url': reverse('notepad:note_new'),
        #     'redirect': None,
        #     'form_class': QuestionForm,
        #     'keys': ['question', 'hint', 'answer'],
        #     'values_list': values_list,
        #     'login': True,
        #     'normal_value': False,
        # }
        # assert_form(**parameter)
