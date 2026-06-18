import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


def generer_qr_code(url: str) -> ContentFile:
    """
    Génère un QR code pointant vers l'URL du profil public.

    Args:
        url: URL complète du profil public

    Returns:
        ContentFile contenant l'image PNG du QR code
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
    buffer.seek(0)

    return ContentFile(buffer.read(), name='qrcode.png')
