"""notepadアプリケーションのテストモジュール"""

from django.urls import reverse


# functions
def create_user(self, wordbook=False):
    """model: userとwordbookを作成する"""
    self.user = User.objects.create_user('test_user', password='password')
    self.wordbook = Note(title='test', user=self.user)
    self.wordbook.save()


def get_url(app_name, kwargs):
    """urlを取得する"""
    if kwargs:
        return reverse(app_name, kwargs=kwargs)
    else:
        return reverse(app_name)


def assert_normal_get_request(self, app_name, kwargs=None, status_code=200):
    """function: Viewのテスト"""
    # request
    url = get_url(app_name, kwargs)
    response = self.client.get(url)
    # assert http status
    self.assertEqual(response.status_code, status_code)


def assert_pagination(
        self, app_name, kwargs=None, page_num=4, list_names=['object_list']):
    """function: paginationのテスト"""
    # request
    url = get_url(app_name, kwargs)
    response = self.client.get(url)
    # assert pagination
    self.assertIn('is_paginated', response.context)
    for list_name in list_names:
        num = len(response.context[list_name])
        self.assertEqual(num, page_num)
