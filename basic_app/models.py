from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    portfolio_site = models.URLField(blank=True)


    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='image_files', blank=True)

    def __str__(self):
        return self.author

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url