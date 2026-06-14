import json
import re
from groq import Groq
from django.conf import settings


client = Groq(api_key=settings.GROQ_API_KEY)


def reparer_json(texte: str) -> str:
    """Répare les erreurs courantes de syntaxe JSON générées par le LLM."""
    texte = re.sub(r'"(\w+)>', r'"\1":', texte)
    return texte


def calculer_score_employabilite(profil_data: dict) -> dict:
    """
    Calcule un score d'employabilité via IA en analysant le profil complet.

    Args:
        profil_data: Dictionnaire contenant les infos du profil
                     (titre, compétences, expériences, formations, projets)

    Returns:
        Dictionnaire avec score, points forts, points faibles, recommandations
    """

    prompt = f"""Tu es un expert en recrutement tech en Afrique de l'Ouest. Analyse ce profil professionnel et donne un score d'employabilité réaliste sur 100.

Profil :
- Titre : {profil_data.get('titre_professionnel', '')}
- Niveau : {profil_data.get('niveau_carriere', '')}
- Compétences techniques : {', '.join(profil_data.get('competences_techniques', []))}
- Soft skills : {', '.join(profil_data.get('soft_skills', []))}
- Formations : {profil_data.get('formations', [])}
- Expériences : {profil_data.get('experiences', [])}
- Projets : {profil_data.get('projets', [])}
- Certifications : {', '.join(profil_data.get('certifications', []))}

Méthode de notation à suivre STRICTEMENT :
- Compétences techniques : jusqu'à 25 points (nombre et pertinence pour le marché tech)
- Expériences professionnelles : jusqu'à 30 points (pertinence et durée)
- Formations : jusqu'à 20 points (niveau et domaine)
- Projets concrets : jusqu'à 15 points (nombre et qualité)
- Certifications : jusqu'à 10 points

Additionne ces sous-scores pour obtenir le score final sur 100.

IMPORTANT : respecte STRICTEMENT la syntaxe JSON, chaque clé suivie de ":".

Retourne UNIQUEMENT ce JSON, sans markdown :
{{
    "score": 75,
    "points_forts": ["point fort 1", "point fort 2", "point fort 3"],
    "points_faibles": ["point faible 1", "point faible 2"],
    "recommandations": ["recommandation 1", "recommandation 2", "recommandation 3"]
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=1000
        )

        brut = response.choices[0].message.content.strip()
        brut = reparer_json(brut)
        return json.loads(brut)

    except json.JSONDecodeError:
        raise ValueError("Le calcul du score a retourné un JSON invalide")

    except Exception as e:
        raise ValueError(f"Erreur lors du calcul du score : {str(e)}")
