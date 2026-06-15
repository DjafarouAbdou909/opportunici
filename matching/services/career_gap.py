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

    prompt = f"""Tu es un conseiller carrière expert en tech, spécialisé Afrique de l'Ouest.

PROFIL ACTUEL :
- Titre actuel : {profil_data.get('titre_professionnel', '')}
- Niveau : {profil_data.get('niveau_carriere', '')}
- Compétences techniques actuelles : {', '.join(profil_data.get('competences_techniques', []))}
- Expériences : {profil_data.get('experiences', [])}
- Projets déjà réalisés : {profil_data.get('projets', [])}

OBJECTIF VISÉ : {objectif}

TÂCHE :
1. Identifie les 5-10 compétences ESSENTIELLES pour devenir {objectif}
2. Compare avec les compétences ACTUELLES du profil
3. "competences_acquises" = intersection (compétences déjà maîtrisées ET pertinentes pour l'objectif)
4. "competences_manquantes" = compétences essentielles NON présentes dans le profil (maximum 5, par ordre de priorité)
5. Pour la roadmap, base-toi sur les projets/expériences EXISTANTS du profil quand c'est pertinent. Propose des actions SPÉCIFIQUES et personnalisées, jamais génériques.

IMPORTANT : respecte STRICTEMENT la syntaxe JSON, chaque clé suivie de ":".

Retourne UNIQUEMENT ce JSON, sans markdown :
{{
    "competences_acquises": ["compétence1", "compétence2"],
    "competences_manquantes": ["compétence1", "compétence2", "compétence3"],
    "plan_30_jours": ["action concrète 1", "action concrète 2", "action concrète 3"],
    "plan_60_jours": ["action concrète 1", "action concrète 2", "action concrète 3"],
    "plan_90_jours": ["action concrète 1", "action concrète 2", "action concrète 3"]
}}

Règles pour les actions de la roadmap :
- INTERDIT : "suivre un cours générique sur Coursera/edX/Udemy" sans précision
- PRÉFÈRE : approfondir une compétence existante via un projet concret lié au contexte du profil
- Chaque action doit nommer une compétence PRÉCISE et un livrable CONCRET (ex: "Construire une API REST avec FastAPI exposant un modèle de classification entraîné sur un dataset public")
- Adapte la difficulté au niveau actuel du profil"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=1500
        )

        brut = response.choices[0].message.content.strip()
        brut = reparer_json(brut)
        return json.loads(brut)

    except json.JSONDecodeError:
        raise ValueError("L'analyse du Career Gap a retourné un JSON invalide")

    except Exception as e:
        raise ValueError(f"Erreur lors de l'analyse Career Gap : {str(e)}")
