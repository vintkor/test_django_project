from django.db import models
from testsite.baseModel import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey


class CatalogCategory(BaseModel, MPTTModel):
    title = models.CharField(verbose_name='Категория', max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    image = models.ImageField(blank=True, default="", upload_to="categories")
    description = RichTextUploadingField(verbose_name="Описание категории", blank=True, default="")
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return "{}".format(self.title)

    def show_image(self):
        """ Показывает превью изображения в админке """
        if self.image:
            return '<img src="{}" width=40>'.format(self.image.url)
        else:
            return "--"

    def get_count_product(self):
        """ Получает количество постов """
        count = CatalogProduct.objects.filter(category=self.id).count()
        return count

    show_image.allow_tags = True
    show_image.short_description = "Изображение"
    get_count_product.short_description = "Кол-во товаров"


class CatalogCurrency(BaseModel):
    title = models.CharField(max_length=100, verbose_name="Название")
    short_title = models.CharField(max_length=5, verbose_name="Сокращение")
    code = models.CharField(max_length=3, verbose_name="Код валюты")
    course = models.DecimalField(verbose_name="Курс", max_digits=10, decimal_places=4)
    is_main = models.BooleanField(verbose_name="Главная")

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return "{}".format(self.title)


class CatalogProduct(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    category = TreeForeignKey(CatalogCategory, blank=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2)
    currency = models.ForeignKey(CatalogCurrency, verbose_name="Валюта", blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=170, blank=True, verbose_name="META DESC", default="")
    text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")

    def __str__(self):
        return "{}".format(self.title)

    def show_image(self):
        """ Показывает превью главного изображения в админке """
        if self.image:
            return '<img src="{}" width=40>'.format(self.image.url)
        else:
            return "--"

    def get_count_comments(self):
        """ Получает количество комментарив поста """
        count = CatalogComment.objects.filter(parent=self.id).count()
        return count

    show_image.allow_tags = True
    show_image.short_description = "Главное изображение"
    get_count_comments.short_description = "Кол-во комментариев"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class CatalogComment(BaseModel):
    parent = models.ForeignKey(CatalogProduct, related_name="parent", verbose_name="Товар коментария")
    text = models.TextField()

    def __str__(self):
        return "Комментарий записи - {}".format(self.parent.title)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class CatalogImage(BaseModel):
    parent = models.ForeignKey(CatalogProduct, related_name="images", verbose_name="Изображение")
    image = models.ImageField(blank=True, default='', upload_to="catalog/product_created-%Y-%m-%d", verbose_name="Изображение")
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")
    is_main = models.BooleanField(default=True, verbose_name="Главное")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return "Изображение товара - {}".format(self.parent.title)

    def show_image(self):
        """ Показывает превью изображения в админке """
        if self.image:
            return '<img src="{}" width=30>'.format(self.image.url)
        else:
            return "--"

    show_image.allow_tags = True
    show_image.short_description = "Изображение"