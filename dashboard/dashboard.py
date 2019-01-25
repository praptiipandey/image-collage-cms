from django.shortcuts import render, redirect
from . import context_processors
# Create your views here.
from account.decorators import my_login_required
from django.views import View

class Dashboard(View):

    @my_login_required
    def get(self, request):
        # if 'user' in request.session:
        context = context_processors.base_variables_all(request)
        return render(request, 'dashboard.html', context)
        # else:
        #     return redirect('login')
