from django.db import models
from django.conf import settings
from profiles.models import Profil
from opportunities.models import Opportunite


class ScoreMatching(models.Model):
    """Score de compatibilité entre un profil et une opportunité."""
    
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='scores_matching'
    )
    opportunite = models.ForeignKey(
        Opportunite,
        on_delete=models.CASCADE,
        related_name='scores_matching'
    )
    score = models.IntegerField(default=0)
    competences_acquises = models.JSONField(default=list)
    competences_manquantes = models.JSONField(default=list)
    explication = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Score Matching'
        unique_together = ['profil', 'opportunite']

    def __str__(self):
        return f"{self.profil} — {self.opportunite} ({self.score}%)"


class ObjectifCarriere(models.Model):
    """Objectif professionnel défini par l'utilisateur."""
    
    profil = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        related_name='objectifs'
    )
    titre_objectif = models.CharField(max_length=200)
    competences_acquises = models.JSONField(default=list)
    competences_manquantes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre_objectif} — {self.profil}"


class Roadmap(models.Model):
    """Feuille de route personnalisée générée par l'IA."""
    
    objectif = models.OneToOneField(
        ObjectifCarriere,
        on_delete=models.CASCADE,
        related_name='roadmap'
    )
    plan_30_jours = models.JSONField(default=list)
    plan_60_jours = models.JSONField(default=list)
    plan_90_jours = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Roadmap — {self.objectif}"