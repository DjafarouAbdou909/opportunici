from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    return render(request, 'profiles/dashboard.html')


@login_required
def upload_cv_view(request):
    return render(request, 'profiles/upload_cv.html')


def public_profile_view(request, username):
    return render(request, 'profiles/public_profile.html')
