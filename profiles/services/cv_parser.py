import json
from groq import Groq
from django.conf import settings


client = Groq(api_key=settings.GROQ_API_KEY)


def analyser_cv(texte_cv: str) -> dict:
    """
    Analyse un CV en texte brut via Groq API et retourne un JSON structuré.

    Args:
        texte_cv: Texte brut extrait du PDF du CV

    Returns:
        Dictionnaire structuré avec les informations du profil
    """

    prompt = f"""Tu es un expert en analyse de CV. Extrais toutes les informations professionnelles de ce CV et retourne UNIQUEMENT un objet JSON valide, sans markdown, sans explication.

Contenu du CV :
{texte_cv}

Structure JSON attendue :
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
    "formation": [{{"diplome": "string", "etablissement": "string", "annee": "string ou null", "domaine": "string ou null"}}],
    "experience": [{{"poste": "string", "entreprise": "string", "duree": "string ou null", "description": "string ou null"}}],
    "projets": [{{"nom": "string", "description": "string ou null", "technologies": ["tech1"]}}],
    "certifications": ["cert1"],
    "niveau_carriere": "etudiant|junior|intermediaire|senior"
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=2000
        )

        brut = response.choices[0].message.content.strip()
        return json.loads(brut)

    except json.JSONDecodeError:
        raise ValueError("Groq a retourné un JSON invalide — réessaie")

    except Exception as e:
        raise ValueError(f"Erreur API Groq : {str(e)}")
