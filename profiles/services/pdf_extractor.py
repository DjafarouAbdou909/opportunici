import io
from pypdf import PdfReader


def extraire_texte_pdf(fichier_pdf) -> str:
    """
    Extrait le texte brut d'un fichier PDF uploadé.
    
    Args:
        fichier_pdf: Fichier PDF uploadé via Django (InMemoryUploadedFile)
        
    Returns:
        Texte brut extrait du PDF
        
    Raises:
        ValueError: Si le PDF est invalide ou vide
    """
    
    try:
        # Lire le fichier en mémoire
        contenu = fichier_pdf.read()
        reader = PdfReader(io.BytesIO(contenu))
        
        if len(reader.pages) == 0:
            raise ValueError("Le PDF est vide.")
        
        texte = ""
        for page in reader.pages:
            texte += page.extract_text() or ""
        
        texte = texte.strip()
        
        if not texte:
            raise ValueError("Impossible d'extraire le texte de ce PDF.")
        
        return texte
    
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du PDF : {str(e)}")
