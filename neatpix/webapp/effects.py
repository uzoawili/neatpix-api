from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps


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


photo_effects = {
    'flip': flip,
    'mirror': mirror,
    'grayscale': grayscale,
    'brighten': brighten,
    'darken': darken,
    'saturate': saturate,
    'blur': blur,
    'detail': detail,
    'smooth': smooth,
    'contrast': contrast,
}
