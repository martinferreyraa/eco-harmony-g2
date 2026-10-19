from io import BytesIO

import qrcode


def imagen_qr(texto):
    """Convierte el texto del QR en una imagen PNG (bytes) para adjuntar."""
    imagen = qrcode.make(texto)
    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    return buffer.getvalue()
