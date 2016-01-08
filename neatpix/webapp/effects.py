from PIL import ImageFilter, ImageEnhance, ImageOps


def thumbnail(image):
    return ImageOps.fit(image, (100, 100))


def smooth(image):
    return image.filter(ImageFilter.SMOOTH)


def invert(image):
    return ImageOps.invert(image)


def flip(image):
    return ImageOps.flip(image)


def mirror(image):
    return ImageOps.mirror(image)


def contrast(image):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(1.5)


def detail(image):
    return image.filter(ImageFilter.EDGE_ENHANCE)


def blur(image):
    return image.filter(ImageFilter.GaussianBlur(radius=3))


def grayscale(image):
    return ImageOps.grayscale(image)


def saturate(image):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(2.0)


def darken(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(0.5)


def brighten(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(1.5)


def charcoal(image):
    image = grayscale(image)
    image = contrast(image)
    image = brighten(image)
    image = detail(image)
    return image


photo_effects = [
    ('saturate', saturate),
    ('grayscale', grayscale),
    ('brighten', brighten),
    ('darken', darken),
    ('blur', blur),
    ('detail', detail),
    ('smooth', smooth),
    ('contrast', contrast),
    ('charcoal', charcoal),
    ('invert', invert),
    ('flip', flip),
    ('mirror', mirror),
]
