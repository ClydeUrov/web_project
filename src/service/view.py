from django.shortcuts import render


def home(request):
    name = 'Boris de Pfeffel Johnson'
    return render(request, 'home.html', {'name': name})
