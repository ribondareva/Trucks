from django import template

register = template.Library()


@register.filter
def get_attr(obj, attr_name):
    try:
        # Сначала пробуем получить атрибут напрямую
        return getattr(obj, attr_name)
    except AttributeError:
        # Если не получилось, пробуем получить как поле формы
        try:
            return obj[attr_name]
        except (KeyError, TypeError):
            return ""


# @register.filter
# def sub(value, arg):
#     return value - arg
#
#
# @register.filter
# def div(value, arg):
#     try:
#         return float(value) / float(arg)
#     except (ValueError, ZeroDivisionError):
#         return 0
#
#
# @register.filter
# def mul(value, arg):
#     return float(value) * float(arg)
