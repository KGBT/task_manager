from django import template

from task.models import UserTask
from user.models import User, UserProfile

register = template.Library()


@register.inclusion_tag('tags/list_employees.html')
def get_employees(auth_user):
    login_user = User.find_by_username(username=auth_user)
    employees = UserProfile.find_employees_by_user(login_user)
    return {'employees': employees}

