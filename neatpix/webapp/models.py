import os

from django.db import models
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.template.defaultfilters import title
from django.dispatch import receiver

from utils import genuid, get_photo_upload_path


class SocialProfile(models.Model):
    """
    Represents information about a user
    authenticated via social media.
    """
    FACEBOOK = '1'
    PROVIDERS = (
        (FACEBOOK, 'Facebook'),
    )

    provider = models.SmallIntegerField(choices=PROVIDERS)
    social_id = models.CharField(max_length=255, unique=True)
    photo = models.TextField(blank=True)
    extra_data = models.TextField(blank=True)

    user = models.OneToOneField(User, related_name='social_profile')

    def __unicode__(self):
        return "{}:{}".format(self.provider, self.social_id)


class Photo(models.Model):
    """
    Represents information about photos
    uploaded by the current user.
    """
    image = models.ImageField(upload_to=get_photo_upload_path, max_length=255)
    public_id = models.CharField(default=genuid, max_length=50)
    caption = models.CharField(max_length=255, blank=True)
    effects = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False, auto_now=True)

    user = models.ForeignKey(User, related_name='photos')

    def serialize(self):
        """
        serializes the photo to a json-style dictionary.
        """
        return {
            'public_id': self.public_id,
            'filename': os.path.basename(self.image.name),
            'username': self.user.username,
            'caption': self.caption,
            'effects': self.effects,
            'date': title(naturalday(self.date_modified)),
        }

    def __unicode__(self):
        return "<Photo: {}-{}".format(self.caption, self.public_id)


@receiver(post_delete, sender=Photo)
def delete_image_file(sender, instance, **kwargs):
    """
    Function that deletes the associated image file
    from the file storage when the Photo instance
    is deleted from the db.
    """
    # get the image file path:
    image_path = instance.image.path
    # delete file from storage:
    if os.path.exists(image_path):
        os.remove(image_path)
