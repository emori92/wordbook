"""notepadアプリケーションのViewsに関するオブジェクトをまとめている"""


# pagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# RankingView
def set_paginator(self, queryset, url_parameter, page_num=12):
    """function: paginationを作成"""
    # paginatorインスタンスを作成
    paginator = Paginator(queryset, page_num)
    page = self.request.GET.get(url_parameter)
    # GETリクエストからpaginationをreturn
    try:
        pagination = paginator.page(page)
    except PageNotAnInteger:
        pagination = paginator.page(1)
    except EmptyPage:
        pagination = paginator.page(paginator.num_pages)
    return pagination


def set_ranking_num(objects):
    """rankingの順位をobjectsに添える"""
    
    if objects.start_index == 1:
        return {n: value for n, value in enumerate(objects, start=1)}
    else:
        # paginationのindex番号を取得する
        num =  objects.start_index()
        return {n: value for n, value in enumerate(objects, start=num)}


def set_ranking(self, context, queryset, url, queryset_name, rankingset_name):
    """function: star, user, tagの共通の処理"""
    # paginatorをもったquerysetを作成
    object_list = set_paginator(self, queryset, url)
    # paginationを利用するためにquerysetも定義
    context[queryset_name] = object_list
    # 
    context[rankingset_name] = set_ranking_num(object_list)
