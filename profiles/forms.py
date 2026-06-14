from django import forms


class UploadCVForm(forms.Form):
    """Formulaire d'upload de CV PDF."""
    
    cv_pdf = forms.FileField(
        label='Ton CV (PDF)',
        help_text='Format PDF uniquement · Taille max 5MB',
        widget=forms.FileInput(attrs={
            'accept': '.pdf',
            'class': 'hidden',
            'id': 'cv-input'
        })
    )
    
    def clean_cv_pdf(self):
        fichier = self.cleaned_data.get('cv_pdf')
        
        if fichier:
            # Vérifier le format
            if not fichier.name.endswith('.pdf'):
                raise forms.ValidationError('Seuls les fichiers PDF sont acceptés.')
            
            # Vérifier la taille
            if fichier.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Le fichier ne doit pas dépasser 5MB.')
        
        return fichier