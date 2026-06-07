from django.shortcuts import render


def landing_view(request):
    """Landing page OpportuniCI."""
    return render(request, 'core/landing.html')