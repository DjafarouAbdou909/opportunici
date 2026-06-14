from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ObjectifCarriereForm
from .services.career_gap import analyser_career_gap
from .models import ObjectifCarriere, Roadmap
from profiles.models import Profil


@login_required
def career_gap_view(request):
    """Vue Career Gap Analyzer."""

    try:
        profil = request.user.profil
    except Profil.DoesNotExist:
        messages.error(request, 'Tu dois d\'abord uploader ton CV pour utiliser cette fonctionnalité.')
        return redirect('profiles:upload_cv')

    objectif_actuel = ObjectifCarriere.objects.filter(profil=profil).order_by('-created_at').first()

    if request.method == 'POST':
        form = ObjectifCarriereForm(request.POST)

        if form.is_valid():
            titre_objectif = form.cleaned_data['titre_objectif']

            try:
                profil_data = {
                    'titre_professionnel': profil.titre_professionnel,
                    'niveau_carriere': profil.niveau_carriere,
                    'competences_techniques': list(profil.competences_techniques.values_list('nom', flat=True)),
                    'experiences': [{'poste': e.poste, 'description': e.description} for e in profil.experiences.all()],
                    'projets': [{'nom': p.nom, 'description': p.description} for p in profil.projets.all()],
                }

                resultat = analyser_career_gap(profil_data, titre_objectif)

                # Sauvegarder l'objectif
                objectif = ObjectifCarriere.objects.create(
                    profil=profil,
                    titre_objectif=titre_objectif,
                    competences_acquises=resultat.get('competences_acquises', []),
                    competences_manquantes=resultat.get('competences_manquantes', [])
                )

                # Sauvegarder la roadmap
                Roadmap.objects.create(
                    objectif=objectif,
                    plan_30_jours=resultat.get('plan_30_jours', []),
                    plan_60_jours=resultat.get('plan_60_jours', []),
                    plan_90_jours=resultat.get('plan_90_jours', [])
                )

                messages.success(request, 'Ta roadmap a été générée avec succès ! 🎯')
                return redirect('matching:career_gap')

            except ValueError as e:
                messages.error(request, f'Erreur : {str(e)}')

            except Exception as e:
                import traceback
                print("ERREUR COMPLÈTE:", traceback.format_exc())
                messages.error(request, 'Une erreur inattendue s\'est produite. Réessaie.')

    else:
        form = ObjectifCarriereForm()

    return render(request, 'matching/career_gap.html', {
        'form': form,
        'objectif': objectif_actuel,
        'roadmap': objectif_actuel.roadmap if objectif_actuel and hasattr(objectif_actuel, 'roadmap') else None
    })
