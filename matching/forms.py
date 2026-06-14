from django import forms


class ObjectifCarriereForm(forms.Form):
    """Formulaire pour définir l'objectif de carrière."""

    titre_objectif = forms.CharField(
        label='Quel est ton objectif de carrière ?',
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'ex: Machine Learning Engineer, Product Manager...',
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-[#2D6A4F] bg-white'
        })
    )
