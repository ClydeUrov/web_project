from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from servants.forms import UserLoginForm


def login_view(request):
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


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # получение данных из запроса POST
        response = request.POST
        email = response.get('email')
        password = response.get('password')
        first_name = response.get('first_name')
        last_name = response.get('last_name')
        username = response.get('name')

        # создание нового объекта MyUser
        User = get_user_model()
        user = User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        print(user)
        # другие действия, которые необходимо выполнить после создания пользователя

        # возвращаем ответ
        return HttpResponse('User created successfully')
    else:
        return HttpResponse('It is not successfully')
