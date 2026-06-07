from django.shortcuts import render

def landing_view(request):
    steps = [
        {'title': 'Upload ton CV', 'description': 'Téléverse ton CV en PDF en quelques secondes.'},
        {'title': 'Analyse IA', 'description': "L'IA extrait automatiquement ton profil complet."},
        {'title': 'Score & Matching', 'description': 'Reçois ton score et des opportunités adaptées.'},
        {'title': 'Progresse', 'description': 'Suis ta roadmap et améliore ton employabilité.'},
    ]
    return render(request, 'core/landing.html', {'steps': steps})