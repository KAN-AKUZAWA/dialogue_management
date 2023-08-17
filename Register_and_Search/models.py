from django.db import models
import hashlib
from django.utils import timezone

class FileUpload(models.Model):
    uploaded_file = models.FileField(upload_to='', null = True)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField() 
    file_hash = models.CharField(max_length=64, unique=True)

    def save(self, *args, **kwargs):
        # ファイルのハッシュ値を計算して保存
        self.created_at = self.created_at + timezone.timedelta(hours=9)
        super().save(*args, **kwargs)

class dialogue(models.Model):
    filename = models.CharField(max_length = 255)
    character = models.CharField(max_length = 255)
    dialogue  = models.CharField(max_length = 1000)
    dialogue_number = models.IntegerField()
    place = models.CharField(max_length = 255, null = True)
    created_date = models.DateTimeField()
    filepath = models.CharField(max_length = 1000)

class Character(models.Model):
    character = models.CharField(max_length = 255)

