import json
import anthropic
from django.conf import settings


client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)


def analyser_cv(texte_cv: str) -> dict:
    """
    Analyse un CV en texte brut via Claude API et retourne un JSON structuré.
    
    Args:
        texte_cv: Texte brut extrait du PDF du CV
        
    Returns:
        Dictionnaire structuré avec les informations du profil
    """
    
    prompt = f"""Tu es un expert en analyse de CV. Extrais toutes les informations professionnelles de ce CV et retourne UNIQUEMENT un objet JSON valide.

Contenu du CV :
{texte_cv}

Retourne UNIQUEMENT cette structure JSON, sans explication, sans markdown :
{{
    "nom_complet": "string",
    "titre_professionnel": "string",
    "email": "string ou null",
    "telephone": "string ou null",
    "localisation": "string ou null",
    "resume": "string ou null",
    "competences_techniques": ["compétence1", "compétence2"],
    "soft_skills": ["compétence1", "compétence2"],
    "langues": ["langue1", "langue2"],
    "formation": [
        {{
            "diplome": "string",
            "etablissement": "string",
            "annee": "string ou null",
            "domaine": "string ou null"
        }}
    ],
    "experience": [
        {{
            "poste": "string",
            "entreprise": "string",
            "duree": "string ou null",
            "description": "string ou null"
        }}
    ],
    "projets": [
        {{
            "nom": "string",
            "description": "string ou null",
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "certifications": ["cert1", "cert2"],
    "niveau_carriere": "etudiant|junior|intermediaire|senior"
}}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        brut = response.content[0].text.strip()
        
        # Nettoyer les balises markdown éventuelles
        if brut.startswith("```"):
            brut = brut.split("```")[1]
            if brut.startswith("json"):
                brut = brut[4:]
        
        return json.loads(brut)
    
    except json.JSONDecodeError:
        raise ValueError("Claude a retourné un JSON invalide — réessaie")
    
    except anthropic.APIError as e:
        raise ValueError(f"Erreur API Claude : {str(e)}")
