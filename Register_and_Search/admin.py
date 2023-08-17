from django.contrib import admin
from .models import FileUpload, dialogue, Character
# Register your models here.

admin.site.register(FileUpload)
admin.site.register(dialogue)
admin.site.register(Character)