# pagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def set_paginator(self, qs, name):
    '''create paginator'''

    paginator = Paginator(qs, 2)
    page = self.request.GET.get(name)
    try:
        pagination = paginator.page(page)
    except PageNotAnInteger:
        pagination = paginator.page(1)
    except EmptyPage:
        pagination = paginator.page(paginator.num_pages)
    return pagination
