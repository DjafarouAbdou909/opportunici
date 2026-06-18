from django.db import models
from django.conf import settings


class Profil(models.Model):
    """Profil professionnel généré automatiquement depuis le CV."""
    
    NIVEAU_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('junior', 'Junior'),
        ('intermediaire', 'Intermédiaire'),
        ('senior', 'Senior'),
    ]
    
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profil'
    )
    titre_professionnel = models.CharField(max_length=200, blank=True)
    resume = models.TextField(blank=True)
    localisation = models.CharField(max_length=200, blank=True)
    niveau_carriere = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='etudiant'
    )
    cv_pdf = models.FileField(upload_to='cvs/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    est_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __str__(self):
        return f"Profil de {self.utilisateur.full_name}"


class CompetenceTechnique(models.Model):
    """Compétence technique extraite du CV."""
    
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='competences_techniques'
    )
    nom = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nom


class SoftSkill(models.Model):
    """Soft skill extrait du CV."""
    
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='soft_skills'
    )
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Formation(models.Model):
    """Formation académique extraite du CV."""
    
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='formations'
    )
    diplome = models.CharField(max_length=200)
    etablissement = models.CharField(max_length=200)
    domaine = models.CharField(max_length=200, blank=True)
    annee = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return f"{self.diplome} — {self.etablissement}"


class Experience(models.Model):
    """Expérience professionnelle extraite du CV."""
    
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    poste = models.CharField(max_length=200)
    entreprise = models.CharField(max_length=200)
    duree = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.poste} — {self.entreprise}"


class Projet(models.Model):
    """Projet extrait du CV."""
    
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='projets'
    )
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.nom


class ScoreEmployabilite(models.Model):
    """Score d'employabilité calculé par l'IA."""
    
    profil = models.OneToOneField(
        Profil,
        on_delete=models.CASCADE,
        related_name='score_employabilite'
    )
    score = models.IntegerField(default=0)
    resume = models.TextField(blank=True, default='')
    points_forts = models.JSONField(default=list)
    points_faibles = models.JSONField(default=list)
    recommandations = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Score {self.score}/100 — {self.profil}"