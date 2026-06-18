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
    Calcule un score d'employabilité riche via IA en analysant le profil complet.

    Args:
        profil_data: Dictionnaire contenant les infos du profil
                     (titre, compétences, expériences, formations, projets)

    Returns:
        Dictionnaire avec score, résumé, points forts détaillés,
        axes de progrès détaillés, et conseils stratégiques
    """

    prompt = f"""Tu es un expert en recrutement tech en Afrique de l'Ouest, reconnu pour tes analyses de CV détaillées et bienveillantes.

Profil à analyser :
- Titre : {profil_data.get('titre_professionnel', '')}
- Niveau : {profil_data.get('niveau_carriere', '')}
- Compétences techniques : {', '.join(profil_data.get('competences_techniques', []))}
- Soft skills : {', '.join(profil_data.get('soft_skills', []))}
- Formations : {profil_data.get('formations', [])}
- Expériences : {profil_data.get('experiences', [])}
- Projets : {profil_data.get('projets', [])}
- Certifications : {', '.join(profil_data.get('certifications', []))}

Méthode de notation à suivre STRICTEMENT pour le score :
- Compétences techniques : jusqu'à 25 points
- Expériences professionnelles : jusqu'à 30 points
- Formations : jusqu'à 20 points
- Projets concrets : jusqu'à 15 points
- Certifications : jusqu'à 10 points

TÂCHE :
1. Calcule le score selon la grille ci-dessus
2. Rédige un résumé qualitatif (2-3 phrases) qui contextualise le profil dans son ensemble, en mentionnant des éléments SPÉCIFIQUES du profil (pas générique)
3. Liste 3 à 5 points forts DÉTAILLÉS (1-2 phrases chacun), en citant des éléments concrets et chiffrés du profil quand possible
4. Liste 3 à 5 axes de progrès DÉTAILLÉS (1-2 phrases chacun), expliquant le "pourquoi" de chaque point, de façon constructive et jamais culpabilisante
5. Donne 3 à 5 conseils stratégiques actionnables et concrets

IMPORTANT : respecte STRICTEMENT la syntaxe JSON, chaque clé suivie de ":".

Retourne UNIQUEMENT ce JSON, sans markdown :
{{
    "score": 75,
    "resume": "string détaillé contextualisant le profil",
    "points_forts": ["point fort détaillé 1", "point fort détaillé 2", "point fort détaillé 3"],
    "points_faibles": ["axe de progrès détaillé 1", "axe de progrès détaillé 2"],
    "recommandations": ["conseil actionnable 1", "conseil actionnable 2", "conseil actionnable 3"]
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=1800
        )

        brut = response.choices[0].message.content.strip()
        brut = reparer_json(brut)
        return json.loads(brut)

    except json.JSONDecodeError:
        raise ValueError("Le calcul du score a retourné un JSON invalide")

    except Exception as e:
        raise ValueError(f"Erreur lors du calcul du score : {str(e)}")
