# pagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def set_paginator(self, queryset, url_parameter):
    '''create paginator'''

    paginator = Paginator(queryset, 4)
    page = self.request.GET.get(url_parameter)
    try:
        pagination = paginator.page(page)
    except PageNotAnInteger:
        pagination = paginator.page(1)
    except EmptyPage:
        pagination = paginator.page(paginator.num_pages)
    return pagination


def set_ranking_num(objects):
    """set ranking num"""
    
    if objects.start_index == 1:
        return {str(n): value for n, value in enumerate(objects, start=1)}
    else:
        # paginationのindex番号を取得する
        num =  objects.start_index()
        return {str(n): value for n, value in enumerate(objects, start=num)}
