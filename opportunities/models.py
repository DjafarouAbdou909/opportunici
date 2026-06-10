from django.db import models


class Opportunite(models.Model):
    """Opportunité professionnelle — emploi, stage, bourse ou hackathon."""
    
    TYPE_CHOICES = [
        ('emploi', 'Emploi'),
        ('stage', 'Stage'),
        ('bourse', 'Bourse'),
        ('hackathon', 'Hackathon'),
        ('bootcamp', 'Bootcamp'),
    ]
    
    titre = models.CharField(max_length=300)
    type_opportunite = models.CharField(max_length=20, choices=TYPE_CHOICES)
    entreprise_ou_org = models.CharField(max_length=200)
    localisation = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    competences_requises = models.JSONField(default=list)
    lien = models.URLField(blank=True)
    date_limite = models.DateField(null=True, blank=True)
    est_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Opportunité'
        verbose_name_plural = 'Opportunités'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titre} — {self.entreprise_ou_org}"