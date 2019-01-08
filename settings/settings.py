from django.shortcuts import render, redirect
from django.views import View
from dashboard import context_processors


class Settings(View):
    def get(self, request):
        if 'user' not in request.session:
            return redirect('login')
        context = context_processors.base_variables_all(request)
        return render(request, "settings/setting.html", context)

    def post(self, request):
       pass



