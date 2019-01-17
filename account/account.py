import random
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import User
from security.models import Api_key
from .salting_hashing import get_salt, hash_string
import hashlib

class LoginView(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        name = request.POST['username']
        password = request.POST['pass']
        authenticate = self.authenticate_user(name, password)
        msg = ""
        if authenticate[0]:
            msg = authenticate[1]
            # if not user.is_active:
            #     msg = "username %s is not active, contact your admin." % name
            # else:
            #     hashed_password = hash_string(user.salt, password)
            #     if hashed_password == user.hashed_password:
            request.session['user'] = authenticate[2]
            key = Api_key.objects.values("key").first()
            if not key:
                h_string = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                sha_signature = hashlib.sha1(h_string.encode()).hexdigest()
                Api_key.objects.create(key=sha_signature)
                request.session['api_key'] = hashlib.md5(sha_signature.encode()).hexdigest()
            else:
                request.session['api_key'] = hashlib.md5(key["key"].encode()).hexdigest()


            return redirect('index')
                # else:
                #     msg = "username password mismatched"
        else:
            msg = authenticate[1]

        return render(request, 'account/login.html', {"msg": msg, "name": name, "password": password})

    @staticmethod
    def authenticate_user(username, password):
        try:
            user = User.objects.get(user_name=username)
        except Exception as e:
            user = None

        result = []
        msg = ""
        status = False
        user_id = ""

        if user:
            if not user.is_active:
                msg = "username %s is not active, contact your admin." % username
            else:
                hashed_password = hash_string(user.salt, password)
                if hashed_password == user.hashed_password:
                    status = True
                    user_id = user.id
                else:
                    msg = "username password mismatched"
        else:
            msg = "username" + " " + username + " " + "doesnot exists"

        result.append(status)
        result.append(msg)
        result.append(user_id)

        return result


class LogoutView(View):
    def get(self, request):
        print("logout")
        a = list(request.session.keys())
        # user_sess = str(request.session.get('user'))
        for k in a:
            # if k != user_sess:
            del request.session[k]

        return render(request, 'account/logout.html')


class SignUpView(View):
    def get(self, request):
        return render(request, 'account/signup.html')

    def post(self, request):
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        confirmpassword = request.POST['pass2']

        if password == confirmpassword:
            try:
                salt = get_salt()
                hashed_password = hash_string(salt, password)
                User.objects.create(user_name=name, email=email, salt=salt, hashed_password=hashed_password, is_superuser=False)
                msg = "successfully registered"
                return render(request, 'account/signup.html', {"msg": msg})
            except Exception as e:
                print(e)

        else:
            msg = "password mismatched"
            return render(request, 'account/signup.html', {"msg": msg,"name": name, "email": email,
                                                           "password": password, "confirmpassword": confirmpassword})

