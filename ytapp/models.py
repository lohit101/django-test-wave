import datetime

from django.conf import settings
from django.db import models

# Create your models here.
class AllUploads(models.Model):
    usernamefk = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    upload = models.CharField(verbose_name="Upload", max_length=200, default="")
    upload_time = models.DateTimeField(verbose_name="Upload time", default=datetime.datetime.now)
    
    def __str__(self):
        return str(self.usernamefk)