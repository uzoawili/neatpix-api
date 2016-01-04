from PIL import ImageFilter


def filter_blur(image):
    return image.filter(ImageFilter.GaussianBlur(radius=7))


def filter_1960ish(image):
    return image.filter(ImageFilter.DETAIL)


photo_effects = {
    'blur': filter_blur,
    '1960ish': filter_1960ish,
}
