# 自定义过滤器（python函数）
# 至少一个参数，最多两个
from django.template import Library


# 创建一个Library类对象
register = Library()


@register.filter
def mod(num):
    """判断是否为偶数"""
    return num%2 == 0


@register.filter
def mod_val(num, val):
    """判断你能否整除"""
    return num % val == 0
