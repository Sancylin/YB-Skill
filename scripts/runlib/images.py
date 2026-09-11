"""Decode screenshots, not just their magic bytes. Pillow is a runtime dependency."""
def verify_image(path):
    try:
        from PIL import Image
    except ImportError:
        return 'Pillow unavailable; install scripts/requirements.txt before screenshot verification'
    try:
        with Image.open(path) as im:
            if im.format not in ('PNG','JPEG','WEBP') or min(im.size)<=0: return 'unsupported image format/dimensions'
            im.verify()
        with Image.open(path) as im: im.load()
    except Exception as error:
        return 'image decode failed: '+str(error)
    return None
