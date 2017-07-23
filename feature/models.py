from django.db import models
from testsite.baseModel import BaseModel


class Feature(BaseModel):
    title = models.CharField(verbose_name="Характеристика", max_length=150)

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return "{}".format(self.title)


class Unit(BaseModel):
    unit = models.CharField(verbose_name="Единица измерения", max_length=150)
    short_name = models.CharField(max_length=30, verbose_name="Краткое название", default='')
    feature = models.ForeignKey(Feature, null=True, default=None, verbose_name="Характеристика", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерений"

    def __str__(self):
        return "{}".format(self.unit)


class Value(BaseModel):
    value = models.CharField(verbose_name="Значение характеристики", max_length=150)
    feature = models.ManyToManyField(Feature, verbose_name="Характеристика")

    class Meta:
        verbose_name = "Значение характеристики"
        verbose_name_plural = "Значения характеристик"

    def __str__(self):
        return "{}".format(self.value)


class Set(BaseModel):
    title = models.CharField(verbose_name="Набор характеристик", max_length=150)
    feature = models.ManyToManyField(Feature, verbose_name="Характеристика")

    class Meta:
        verbose_name = "Набор характеристик"
        verbose_name_plural = "Наборы характеристик"

    def __str__(self):
        return "{}".format(self.title)
