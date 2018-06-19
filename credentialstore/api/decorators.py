from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group


def admin_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in
    and a member of the Administrators group, redirecting
    to the log-in page if necessary.
    """
    if user_passes_test(lambda u: Group.objects.get(name='Administrator') in u.groups.all()):
        actual_decorator = user_passes_test(
            lambda u: u.is_authenticated and Group.objects.get(name='Administrator') in u.groups.all(),
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )
    else:
        actual_decorator = user_passes_test(
            lambda u: False,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )

    if function:
        return actual_decorator(function)
    return actual_decorator


def create_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in
    and a member of the Administrators group, redirecting
    to the log-in page if necessary.
    """
    if user_passes_test(lambda u: Group.objects.get(name='Create') in u.groups.all()):
        actual_decorator = user_passes_test(
            lambda u: u.is_authenticated and Group.objects.get(name='Create') in u.groups.all(),
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )
    else:
        actual_decorator = user_passes_test(
            lambda u: False,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )

    if function:
        return actual_decorator(function)
    return actual_decorator


def update_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in
    and a member of the Administrators group, redirecting
    to the log-in page if necessary.
    """
    if user_passes_test(lambda u: Group.objects.get(name='Update') in u.groups.all()):
        actual_decorator = user_passes_test(
            lambda u: u.is_authenticated and Group.objects.get(name='Update') in u.groups.all(),
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )
    else:
        actual_decorator = user_passes_test(
            lambda u: False,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )

    if function:
        return actual_decorator(function)
    return actual_decorator