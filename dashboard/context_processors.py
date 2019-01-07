from django.shortcuts import redirect
from account.models import User, Role, Role_permission, User_role, Permission
from django.db import connection
import json, os

def base_variables_all(request):
    if 'user' not in request.session:
        context = None
    else:

        user_own = User.objects.get(id=request.session['user'])

        permission_user = get_permission(user_own.id)

        context = {"user_own": user_own, "permission_user": permission_user, "nav_sidebar": nav_sidebar()}

    return context


def get_permission(user_id):
    user_groups = User_role.objects.filter(user_id=user_id).values("role_id")
    permission_user = []

    for user_group in user_groups:
        group_permissions = Role_permission.objects.filter(role_id=user_group['role_id']).values("permission_id")
        for group_permission in group_permissions:
            user_permissions = Permission.objects.filter(id=group_permission["permission_id"]).values("content_type_id")
            for user_permission in user_permissions:
                permission_user.append(user_permission["content_type_id"])

    permission_user = list(set(permission_user))
    return permission_user

def nav_sidebar():
    with open("/var/www/django_cms/config.json") as f:
        data = json.load(f)

    return data["nav_sidebar"]