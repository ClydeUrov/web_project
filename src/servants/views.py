from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token

from servants.forms import UserLoginForm


@csrf_exempt
def register(request):
    print("POST:", request.POST)
    print("BODY:", request.body)
    if request.method == 'POST':
        print(2)
        # получение данных из запроса POST
        response = request.POST
        email = response.get('email')
        password = response.get('password')
        first_name = response.get('first_name')
        last_name = response.get('last_name')
        username = response.get('name')

        # создание нового объекта User
        User = get_user_model()
        user = User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        print(user)
        # другие действия, которые необходимо выполнить после создания пользователя

        # возвращаем ответ
        return HttpResponse('User created successfully')
    else:
        return HttpResponse('It is not successfully')


def login_view(request):
    print(111)
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        _next = _next or "/"
        return redirect(_next)
    return render(request, 'servants/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')



