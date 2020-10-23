"""accounts/notepadのテストモジュール"""


from django.urls import reverse
from accounts.models import User
from notepad.models import Note
# selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# functions
def create_user(self, wordbook=False):
    """model: userとwordbookを作成する"""
    self.user = User.objects.create_user('test_user', password='password')
    if wordbook:
        self.wordbook = Note(title='test_title', user=self.user)
        self.wordbook.save()


def assert_normal_get_request(self, url, status_code=200):
    """function: Viewのテスト"""
    # request
    response = self.client.get(url)
    # assert http status
    self.assertEqual(response.status_code, status_code)


def assert_pagination(self, url, pagination_list, page_num=0):
    """function: paginationのテスト"""
    # request
    response = self.client.get(url)
    # assert pagination
    # if page_num:
    self.assertIn('is_paginated', response.context)
    for list_name in pagination_list:
        num = len(response.context[list_name])
        self.assertEqual(num, page_num)
    # else:
    #     for list_name in pagination_list:
    #         # self.assertNotIn('is_paginated', response.context)
    #         num = len(response.context[list_name])
    #         # self.assertNotEqual(num, page_num)


def run_selenium_js_btn(self, url, id_list, class_list, text_list, pagination_list=None):
    """function: ボタン押すと表示切り替わるか"""
    # get request
    home = 'localhost:8000'
    self.selenium.get(f'{home}{url}')
    # wait until rendering
    main_id = id_list[0]
    WebDriverWait(self.selenium, 10) \
        .until(EC.presence_of_element_located((By.ID, main_id)))
    # assert: ボタンを押して表示が変わるか（DBのデータなし）
    for id, text in zip(id_list, text_list):
        btn = self.selenium.find_element_by_id(f'{id}-btn')
        btn.click()
        # 対象の要素を取得し、想定される出力と同じか確認
        elem = self.selenium.find_element_by_id(id) \
            .find_element_by_tag_name('p')
        predict_text = f'{text}がありません。'
        self.assertEqual(elem.text, predict_text)
    # ユーザとwordbookを作成しページを更新
    create_user(self, wordbook=True)
    self.selenium.refresh()
    WebDriverWait(self.selenium, 10) \
        .until(EC.presence_of_element_located((By.ID, main_id)))
    # assert: ボタンを押して表示が変わるか（DBのデータあり）
    for id, text_class, text in zip(id_list, class_list, text_list):
        btn = self.selenium.find_element_by_id(f'{id}-btn')
        btn.click()
        # 対象の要素を取得し、想定される出力と同じか確認
        elem = self.selenium.find_element_by_id(id) \
            .find_element_by_class_name(text_class)
        self.assertEqual(elem.text, predict_text)
