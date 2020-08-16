from django import template


register = template.Library()

# 引数2つをlistにする
@register.filter
def make_list(v1, v2):
    return (v1, v2)
