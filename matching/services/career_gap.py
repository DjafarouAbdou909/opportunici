import json
import re
from groq import Groq
from django.conf import settings


client = Groq(api_key=settings.GROQ_API_KEY)


def reparer_json(texte: str) -> str:
    """Répare les erreurs courantes de syntaxe JSON générées par le LLM."""
    texte = re.sub(r'"(\w+)>', r'"\1":', texte)
    return texte


def analyser_career_gap(profil_data: dict, objectif: str) -> dict:
    """
    Analyse l'écart entre le profil actuel et l'objectif de carrière visé.

    Args:
        profil_data: Dictionnaire avec compétences, expériences, formations
        objectif: Titre du poste/objectif visé (ex: "Machine Learning Engineer")

    Returns:
        Dictionnaire avec compétences acquises, manquantes et roadmap 30/60/90 jours
    """

    prompt = f"""Tu es un conseiller carrière expert en tech. Un étudiant a ce profil et vise cet objectif.

Profil actuel :
- Titre : {profil_data.get('titre_professionnel', '')}
- Niveau : {profil_data.get('niveau_carriere', '')}
- Compétences techniques : {', '.join(profil_data.get('competences_techniques', []))}
- Expériences : {profil_data.get('experiences', [])}
- Projets : {profil_data.get('projets', [])}

Objectif visé : {objectif}

IMPORTANT : respecte STRICTEMENT la syntaxe JSON, chaque clé suivie de ":".

Retourne UNIQUEMENT ce JSON, sans markdown :
{{
    "competences_acquises": ["compétence1", "compétence2"],
    "competences_manquantes": ["compétence1", "compétence2", "compétence3"],
    "plan_30_jours": ["action 1", "action 2", "action 3"],
    "plan_60_jours": ["action 1", "action 2", "action 3"],
    "plan_90_jours": ["action 1", "action 2", "action 3"]
}}

Sois concret, réaliste et orienté action. Chaque action doit être spécifique (ex: "Suivre le cours X sur Y", "Construire un projet Z")."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=1500
        )

        brut = response.choices[0].message.content.strip()
        brut = reparer_json(brut)
        return json.loads(brut)

    except json.JSONDecodeError:
        raise ValueError("L'analyse du Career Gap a retourné un JSON invalide")

    except Exception as e:
        raise ValueError(f"Erreur lors de l'analyse Career Gap : {str(e)}")
