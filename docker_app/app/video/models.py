from django.db import models


# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=101, verbose_name='title')
    mix = models.CharField(max_length=7)
    has_prew = models.BooleanField(default=False)
    has_mp4 = models.BooleanField(default=False)
    has_webm = models.BooleanField(default=False)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['title', 'mix'], name='no_duplicate')]
