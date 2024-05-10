from user.models import User


def get_employees(request):
    user = request.user
    user_log = User.find_by_username('nikitin')  # заглушка
    return {'employees': user_log.get_employees()}
