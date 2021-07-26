from django.shortcuts import render
from .forms import CustomUserForm
from .models import CustomUser
from django.contrib.auth.models import User


def get_name(request):
    context = {}
    user = request.user
    context['user'] = CustomUser.objects.get(user=User.objects.get(user)).get_sex_display()
    print(context)
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            context['form'] = form
            print(context)
            return render(request, 'home.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomUserForm()
        context['form'] = form
        print(context)
    print(context)
    return render(request, 'home.html', context)
