from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Group)
admin.site.register(models.Section)
admin.site.register(models.Post)
admin.site.register(models.Replie)
admin.site.register(models.Stat)
admin.site.register(models.Comment)

