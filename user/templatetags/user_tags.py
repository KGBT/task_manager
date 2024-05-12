from django import template

from task.models import UserTask

register = template.Library()


@register.inclusion_tag('tags/list_employees.html')
def get_employees(auth_user):
    employees = auth_user.get_employees()
    return {'employees': employees}


