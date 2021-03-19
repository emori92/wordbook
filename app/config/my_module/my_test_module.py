"""accounts/notepadのテストモジュール"""


from django.urls import reverse
from accounts.models import User
from notepad.models import Note
# selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# test: form
def assert_form(
    self, url, redirect, form_class, keys, values_list, login, normal_value):
    """test form: values_listの長さに応じてcheck_form_validationを実行する"""
    # length values_list
    li_len = len(values_list)
    # value list
    meta_value = [values[0] for values in values_list]
    # test
    for num, values in enumerate(values_list):
        # form inputが1つの場合
        if li_len == 1:
            # function parameter
            params = {}
            key = keys[0]
        # form inputが2つの場合
        if li_len == 2:
            # function parameter
            if num == 0:
                params = {keys[1]: meta_value[1]}
                key = keys[0]
            else:
                params = {keys[0]: meta_value[0]}
                key = keys[1]
        # form inputが3つの場合
        if li_len == 3:
            # function parameter
            if num == 0:
                params = {keys[1]: meta_value[1], keys[2]: meta_value[2]}
                key = keys[0]
            elif num == 1:
                params = {keys[0]: meta_value[0], keys[2]: meta_value[2]}
                key = keys[1]
            else:
                params = {keys[0]: meta_value[0], keys[1]: meta_value[1]}
                key = keys[2]
        # check validation
        check_form_validation(
            self, url, redirect, form_class, key,
            values, params, login, normal_value)


def check_form_validation(
    self, url, redirect, form_class, key, values, params, login, normal_value):
    """test form : formのvalidation、status code、redirectを確認"""
    for value in values:
        # form
        params[key] = value
        form = form_class(params)
        # 正常値
        if normal_value:
            # validation
            self.assertTrue(form.is_valid())
            # response
            if login:
                self.client.login(username='test_user', password='password')
            response = self.client.post(url, params)
            # status code
            self.assertEqual(response.status_code, 302)
            # redirect
            self.assertRedirects(response, redirect)
        # 異常値
        else:
            # validation
            self.assertFalse(form.is_valid())
            # response
            if login:
                self.client.login(username='test_user', password='password')
            response = self.client.post(url, params)
            # status code
            self.assertEqual(response.status_code, 200)


# test: view
def create_user(self, wordbook=False):
    """test view: userとwordbookを作成する"""
    self.user = User.objects.create_user('test_user', password='password')
    if wordbook:
        self.wordbook = Note(title='test_title', user=self.user)
        self.wordbook.save()


def assert_normal_get_request(self, url, status_code=200):
    """test view: Viewのテスト"""
    # request
    response = self.client.get(url)
    # assert http status
    self.assertEqual(response.status_code, status_code)


def assert_pagination(self, url, pagination_list, page_num):
    """test view: paginationのテスト"""
    # request
    response = self.client.get(url)
    # pagination
    # if page_num:
    # paginationがあるかテスト
    self.assertIn('is_paginated', response.context)
    # 各object_listで、paginationの数値が一致しているか確認
    for list_name in pagination_list:
        num = len(response.context[list_name])
        self.assertEqual(num, page_num)
    # else:
    #     for list_name in pagination_list:
    #         # self.assertNotIn('is_paginated', response.context)
    #         num = len(response.context[list_name])
    #         # self.assertNotEqual(num, page_num)


def redirect_dashboard(self, url):
    """test view: login後、home/login/signupにアクセスするとdashboardへredirectする"""
    # if login, redirect to dashboard
    create_user(self)
    self.client.login(username='test_user', password='password')
    # check redirect
    redirect_url = reverse('notepad:dashboard', kwargs={'pk': self.user.pk})
    response = self.client.get(url)
    self.assertRedirects(response, redirect_url)


def login_selenium(self):
    """test view: seleniumでログイン"""
    # access
    domain = '127.0.0.1:8000'
    # GET request
    self.selenium.get(f'{domain}{reverse("accounts:login")}')
    # input form values
    login = self.selenium.find_element_by_name('username')
    login.send_keys('admin')
    password = self.selenium.find_element_by_name('password')
    password.send_keys('hogemori')
    # login
    btn = self.selenium.find_element_by_id('login-btn')
    btn.click()


def run_selenium_js_btn(self, url, id_list, class_list, text_list):
    """test view: ボタン押すと表示切り替わるか"""
    # get request
    home = 'localhost:8000'
    self.selenium.get(f'{home}{url}')
    # wait until rendering
    main_id = id_list[0]
    WebDriverWait(self.selenium, 4).until(
        EC.presence_of_element_located((By.ID, main_id)))
    # assert: ボタンを押して表示が変わるか（DBのデータあり）
    for id, text_class, text in zip(id_list, class_list, text_list):
        btn = self.selenium.find_element_by_id(f'{id}-btn')
        btn.click()
        # 対象の要素を取得し、想定される出力と同じか確認
        elem = self.selenium.find_element_by_id(
            id).find_element_by_class_name(text_class)
        self.assertEqual(elem.text, text)
