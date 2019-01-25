from django.shortcuts import redirect
from django.core import handlers
def my_login_required(function):
    def wrapper(object, *args, **kw):

        if not ('user' in object.request.session and object.request.session.get('user')):
            return redirect('login')
        else:
            return function(object, *args, **kw)

    return wrapper
