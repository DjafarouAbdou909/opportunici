from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm


def signup_view(request):
    """Vue d'inscription."""
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name} ! Ton compte est créé.')
            return redirect('profiles:dashboard')
        else:
            messages.error(request, 'Vérifie les informations saisies.')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Vue de connexion."""
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bon retour {user.first_name} !')
            return redirect('profiles:dashboard')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Vue de déconnexion."""
    logout(request)
    messages.info(request, 'Tu es déconnecté.')
    return redirect('accounts:login')