from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token

from servants.forms import UserLoginForm

User = get_user_model()

@csrf_exempt
def register(request):
    if request.method == 'POST':

        response = request.POST
        email = response.get('email')
        password = response.get('password')
        first_name = response.get('first_name')
        last_name = response.get('last_name')
        username = response.get('name')

        user = User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name, username=username
        )

        return HttpResponse('User created successfully!')
    else:
        return redirect('home')


def login_view(request):
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        _next = _next or "/"
        return redirect('servants:user')
    return render(request, 'servants/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('servants:login')


def user_view(request):
    user_id = request.user.id
    print(request)
    user = User.objects.get(id=user_id)
    first_name = user.first_name  # "Clyde"
    last_name = user.last_name
    print(first_name)
    print(last_name)
    context = {
        'email': user.email,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
    }
    return render(request, 'servants/user.html', context)



