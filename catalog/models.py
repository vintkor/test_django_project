from django.db import models
from testsite.baseModel import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from feature.models import Set, Feature, Unit, Value


class CatalogCategory(BaseModel, MPTTModel):
    title = models.CharField(verbose_name='Категория', max_length=255)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, default='')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    image = models.ImageField(blank=True, default="", upload_to="categories")
    description = RichTextUploadingField(verbose_name="Описание категории", blank=True, default="")
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")
    feature_set = models.ManyToManyField(Set, verbose_name="Набор характеристик")

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
    slug = models.SlugField(verbose_name="Слаг", max_length=255, default='')
    category = TreeForeignKey(CatalogCategory, blank=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2)
    currency = models.ForeignKey(CatalogCurrency, verbose_name="Валюта", blank=True, null=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(Unit, verbose_name="Единица измерения", default=None, on_delete=models.SET_NULL, null=True)
    step = models.DecimalField(verbose_name="Шаг", max_digits=8, decimal_places=3, default=1)
    description = models.CharField(max_length=170, blank=True, verbose_name="META DESC", default="")
    text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")
    image = models.ImageField(verbose_name="Изображение", blank=True, default='', upload_to="catalog/product_created-%Y-%m-%d")
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

    def get_all_images(self):
        return CatalogImage.objects.filter(active=True, parent=self)

    def get_price_in_main_currency(self):
        return self.currency.course * self.price

    def save(self, *args, **kwargs):
        if self.category:
            super(CatalogProduct, self).save(*args, **kwargs)
            for s in Set.objects.filter(catalogcategory=self.category):
                for f in Feature.objects.filter(set=s):
                    try:
                        ProductFeature.objects.get(product=self, feature=f)
                    except ProductFeature.DoesNotExist:
                        feature = ProductFeature(product=self, feature=f)
                        feature.save()

    show_image.allow_tags = True
    show_image.short_description = "Главное изображение"
    get_count_comments.short_description = "Кол-во комментариев"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductFeature(BaseModel):
    feature = models.ForeignKey(Feature, default=None, null=True, verbose_name="арактеристака", on_delete=models.SET_NULL)
    value = models.CharField(default=None, null=True, blank=True, verbose_name="Значение", max_length=150)
    unit = models.ForeignKey(Unit, default=None, blank=True, null=True, verbose_name="Единица измерения", on_delete=models.SET_NULL)
    product = models.ForeignKey(CatalogProduct, default=None, null=True, verbose_name="Товар", on_delete=models.SET_NULL)


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
