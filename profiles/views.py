from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import UploadCVForm
from .services.pdf_extractor import extraire_texte_pdf
from .services.cv_parser import analyser_cv
from .models import (
    Profil, CompetenceTechnique, SoftSkill,
    Formation, Experience, Projet, ScoreEmployabilite
)
import uuid


@login_required
def dashboard_view(request):
    """Dashboard principal de l'utilisateur."""
    try:
        profil = request.user.profil
    except Profil.DoesNotExist:
        profil = None
    
    return render(request, 'profiles/dashboard.html', {
        'profil': profil
    })


@login_required
def upload_cv_view(request):
    """Vue upload CV avec analyse IA."""
    
    if request.method == 'POST':
        form = UploadCVForm(request.POST, request.FILES)
        
        if form.is_valid():
            fichier = form.cleaned_data['cv_pdf']
            
            try:
                # Extraire le texte du PDF
                texte_cv = extraire_texte_pdf(fichier)
                
                # Analyser avec l'IA
                donnees_profil = analyser_cv(texte_cv)
                
                #Sauvegarder le profil
                try:
                    profil = Profil.objects.get(utilisateur=request.user)
                except Profil.DoesNotExist:
                    profil = Profil(
                        utilisateur=request.user,
                        slug=str(uuid.uuid4())[:8]
                    )
                profil.titre_professionnel = donnees_profil.get('titre_professionnel') or ''
                profil.resume = donnees_profil.get('resume') or ''
                profil.localisation = donnees_profil.get('localisation') or ''
                profil.niveau_carriere = donnees_profil.get('niveau_carriere', 'etudiant')
                
                if not profil.slug:
                    profil.slug = str(uuid.uuid4())[:8]
                
                profil.save()
                
                # Sauvegarder les compétences
                CompetenceTechnique.objects.filter(profil=profil).delete()
                for competence in donnees_profil.get('competences_techniques') or []:
                    CompetenceTechnique.objects.create(
                        profil=profil,
                        nom=competence
                    )
                
                # Sauvegarder les soft skills
                SoftSkill.objects.filter(profil=profil).delete()
                for skill in donnees_profil.get('soft_skills') or []:
                    SoftSkill.objects.create(profil=profil, nom=skill)
                
                # Sauvegarder les formations
                Formation.objects.filter(profil=profil).delete()
                for formation in donnees_profil.get('formation') or []:
                    Formation.objects.create(
                        profil=profil,
                        diplome=formation.get('diplome', ''),
                        etablissement=formation.get('etablissement', ''),
                        domaine=formation.get('domaine', ''),
                        annee=formation.get('annee', '')
                    )
                
                # Sauvegarder les expériences
                Experience.objects.filter(profil=profil).delete()
                for exp in donnees_profil.get('experience') or []:
                    Experience.objects.create(
                        profil=profil,
                        poste=exp.get('poste', ''),
                        entreprise=exp.get('entreprise', ''),
                        duree=exp.get('duree', ''),
                        description=exp.get('description', '')
                    )
                
                # Sauvegarder les projets
                Projet.objects.filter(profil=profil).delete()
                for projet in donnees_profil.get('projets') or []:
                    Projet.objects.create(
                        profil=profil,
                        nom=projet.get('nom', ''),
                        description=projet.get('description', ''),
                        technologies=', '.join(projet.get('technologies', []))
                    )
                
                messages.success(request, 'Ton profil a été généré avec succès ! 🎉')
                return redirect('profiles:dashboard')
            
            except ValueError as e:
                messages.error(request, f'Erreur : {str(e)}')
            
            except Exception as e:
                import traceback
                print("ERREUR COMPLÈTE:", traceback.format_exc())
                messages.error(request, 'Une erreur inattendue s\'est produite. Réessaie.')
        
    else:
        form = UploadCVForm()
    
    return render(request, 'profiles/upload_cv.html', {'form': form})


@login_required
def public_profile_view(request, username):
    """Vue profil public."""
    from django.shortcuts import get_object_or_404
    from accounts.models import User
    
    utilisateur = get_object_or_404(User, username=username)
    profil = get_object_or_404(Profil, utilisateur=utilisateur, est_public=True)
    
    return render(request, 'profiles/public_profile.html', {
        'profil': profil
    })