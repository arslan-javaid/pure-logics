from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class Home(TemplateView):
    template_name = 'authenticate/home.html'

    def get(self, request):
        return render(request, self.template_name, {})


class Authentication(TemplateView):
    template_login = 'authenticate/login.html'
    template_home = 'authenticate/home.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_home, {})
        else:
            return render(request, self.template_login, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!!!')
            # Redirect to a success page.
            return render(request, self.template_home, {'alert': 'alert-success'})
        else:
            messages.success(request, 'Error Logged in - Please try again...')
            # Return an 'invalid login' error message.
            return render(request, self.template_login, {'alert': 'alert-danger'})


class LogoutView(View):
    template_name = 'authenticate/home.html'

    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out!!!')
        return render(request, self.template_name, {'alert': 'alert-success'})
