from django.shortcuts import render, redirect
from django.views import View
from dashboard import context_processors
from account.decorators import my_login_required

class Settings(View):

    @my_login_required
    def get(self, request):
        # if 'user' not in request.session:
        #     return redirect('login')
        context = context_processors.base_variables_all(request)
        return render(request, "settings/setting.html", context)

    @my_login_required
    def post(self, request):
       pass



