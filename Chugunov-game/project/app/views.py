from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm
from .models import User, Skin


def registration_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            fio = request.POST.get('fio')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create(fio=fio, email=email, password=password, username=email)
            return redirect('login')
        return render(request, 'registration.html', context={"form": form, "error": form.errors})
    return render(request, 'registration.html', context={'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = "Неверный email или пароль"
                return render(request, 'login.html',
                              {'form': form, 'error': error})
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def home_page(request):
    user = request.user
    if user.is_authenticated:
        skin = Skin.objects.get(id=1)
        user.skins.add(skin)
        skin = request.user.skins.all()
        return render(request, 'home.html', context={'user': user, 'skins': skin})
    return render(request, 'home.html', context={'user': user})


def shop_view(request):
    skins = Skin.objects.all()
    user= request.user
    return render(request, 'shop.html', context={"skins": skins, "user": user})


def shop_add_view(request, id):
    user = request.user
    skin = Skin.objects.get(id=id)
    if user.money >= skin.price:
        user.skins.add(skin)
        user.money -= skin.price
        user.save()
        return redirect('home')
    return redirect("shop")


def add_money(request, ball):
    user = request.user
    user.money += ball
    user.save()
    return redirect('home')
