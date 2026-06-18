import json
import re
from groq import Groq
from django.conf import settings


client = Groq(api_key=settings.GROQ_API_KEY)


def reparer_json(texte: str) -> str:
    """Répare les erreurs courantes de syntaxe JSON générées par le LLM."""
    texte = re.sub(r'"(\w+)>', r'"\1":', texte)
    return texte


def normaliser_resultat(resultat: dict) -> dict:
    """
    Corrige les clés alternatives que le LLM peut utiliser par erreur,
    pour garantir un format cohérent attendu par le template.
    """
    competences_corrigees = []
    for comp in resultat.get('competences_manquantes', []):
        if isinstance(comp, dict):
            nom = comp.get('nom') or comp.get('competence') or ''
            competences_corrigees.append({
                'nom': nom,
                'priorite': comp.get('priorite', 'Moyenne'),
                'description': comp.get('description', '')
            })
        else:
            competences_corrigees.append({'nom': str(comp), 'priorite': 'Moyenne', 'description': ''})
    resultat['competences_manquantes'] = competences_corrigees

    for cle_plan in ['plan_30_jours', 'plan_60_jours', 'plan_90_jours']:
        actions_corrigees = []
        for action in resultat.get(cle_plan, []):
            if isinstance(action, dict):
                actions_corrigees.append({
                    'action': action.get('action') or action.get('titre') or '',
                    'objectif': action.get('objectif') or action.get('but') or '',
                    'competence_utilisee': action.get('competence_utilisee') or action.get('competence') or ''
                })
            else:
                actions_corrigees.append({'action': str(action), 'objectif': '', 'competence_utilisee': ''})
        resultat[cle_plan] = actions_corrigees

    return resultat


def analyser_career_gap(profil_data: dict, objectif: str) -> dict:
    """
    Analyse l'écart réel entre le profil actuel et l'objectif de carrière,
    et génère une roadmap progressive 30/60/90 jours.

    Args:
        profil_data: Dictionnaire avec compétences, expériences, formations, projets
        objectif: Titre du poste/objectif visé (ex: "Machine Learning Engineer")

    Returns:
        Dictionnaire avec compétences acquises, manquantes et roadmap 30/60/90 jours
    """

    prompt = f"""Tu es un expert en analyse de carrière et en ingénierie pédagogique.

Ta tâche est d'analyser un profil utilisateur et un objectif de carrière pour produire un diagnostic de gap de compétences et un plan d'évolution.

PROFIL UTILISATEUR :
- Titre actuel : {profil_data.get('titre_professionnel', '')}
- Niveau : {profil_data.get('niveau_carriere', '')}
- Compétences techniques : {', '.join(profil_data.get('competences_techniques', []))}
- Expériences : {profil_data.get('experiences', [])}
- Projets déjà réalisés : {profil_data.get('projets', [])}

OBJECTIF DE CARRIÈRE : {objectif}

RÈGLES CRITIQUES

1. competences_acquises
- uniquement les compétences directement transférables à l'objectif
- exclure tout ce qui est marginal ou hors-sujet
- liste simple de strings

2. competences_manquantes
- maximum 5 compétences
- DOIVENT être classées par priorité réelle (impact sur l'objectif)
- ne jamais lister tout le domaine
- chaque compétence doit représenter un "bloc manquant critique" : pose-toi la question "l'utilisateur peut-il raisonnablement atteindre cet objectif SANS cette compétence ?" — si oui, elle n'est pas prioritaire
- pour CHAQUE compétence manquante, remplis OBLIGATOIREMENT les 3 champs : nom, priorite (Haute/Moyenne/Basse), description (1 phrase expliquant pourquoi c'est important)

3. plans (30/60/90 jours)
Chaque action doit :
- être spécifique au profil utilisateur
- utiliser une compétence déjà acquise comme point de départ
- inclure une progression logique vers l'objectif
- être concrète (projet, exercice, implémentation, build)
- pour CHAQUE action, remplis OBLIGATOIREMENT les 3 champs : action (le projet/exercice concret à faire), objectif (1 phrase expliquant ce que ça apporte vers l'objectif final, JAMAIS vide), competence_utilisee (la compétence de départ utilisée)

Interdiction absolue :
- actions génériques ("suivre un cours", "apprendre Python", "regarder des tutoriels")
- champ "objectif" vide ou manquant dans les actions de roadmap

STYLE
- motivant mais réaliste
- pas de culpabilisation
- orienté ingénierie et progression

CONTRAINTE JSON
- sortie STRICTEMENT JSON valide
- aucune explication hors JSON
- pas de texte avant ou après
- respecte EXACTEMENT la structure ci-dessous, tous les champs sont obligatoires et ne doivent jamais être vides

Format attendu :
{{
    "competences_acquises": ["string", "string"],
    "competences_manquantes": [
        {{"nom": "string", "priorite": "Haute", "description": "string"}}
    ],
    "plan_30_jours": [
        {{"action": "string", "objectif": "string", "competence_utilisee": "string"}}
    ],
    "plan_60_jours": [
        {{"action": "string", "objectif": "string", "competence_utilisee": "string"}}
    ],
    "plan_90_jours": [
        {{"action": "string", "objectif": "string", "competence_utilisee": "string"}}
    ]
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=2000
        )

        brut = response.choices[0].message.content.strip()
        brut = reparer_json(brut)
        return json.loads(brut)

    except json.JSONDecodeError:
        raise ValueError("L'analyse du Career Gap a retourné un JSON invalide")

    except Exception as e:
        raise ValueError(f"Erreur lors de l'analyse Career Gap : {str(e)}")
