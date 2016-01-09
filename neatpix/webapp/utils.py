import os
from time import time
from hashids import Hashids
from django.conf import settings


def genuid(
    salt=settings.SECRET_KEY,
    min_length=settings.UID_LENGTH,
    alphabet=settings.UID_ALPHABET
):
    hashids = Hashids(salt=salt, min_length=min_length, alphabet=alphabet)
    uid = hashids.encode(int(time() * 1000))
    return uid


def get_photo_upload_path(instance, filename):
    """
    This function is called to obtain the upload path
    (relative to MEDIA_ROOT) including the filename for
    the Photo file to be saved to disk.
    """
    name, ext = os.path.splitext(filename)
    new_filename = "{}.{}".format(instance.public_id, ext)
    user_slug = "{}_{}".format(
        instance.user.username,
        instance.user.id
    )
    upload_path = "photos/{}/{}".format(
        user_slug,
        new_filename
    )
    return upload_path
