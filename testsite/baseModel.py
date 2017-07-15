from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Дата обновления")

    objects = models.Manager()
