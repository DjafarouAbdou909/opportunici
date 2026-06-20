import qrcode
import base64
from io import BytesIO


def generer_qr_code_base64(url: str) -> str:
    """
    Génère un QR code en base64, sans le stocker en fichier sur disque.
    Utile en production où le stockage de fichiers n'est pas persistant.

    Args:
        url: URL complète du profil public

    Returns:
        Chaîne base64 prête à être utilisée dans un attribut src="data:image/png;base64,..."
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#2D6A4F", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"
