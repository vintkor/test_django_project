from django.db import models
from testsite.baseModel import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel, BaseModel):
    category_title = models.CharField(max_length=255, verbose_name="Категория")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    category_image = models.ImageField(blank=True, default="", upload_to="categories")
    category_description = RichTextUploadingField(verbose_name="Описание категории", blank=True, default="")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    class MPTTMeta:
        order_insertion_by = ['category_title']

    def __str__(self):
        return "{}".format(self.category_title)

    def show_image(self):
        """ Показывает превью изображения в админке """
        if self.category_image:
            return '<img src="{}" width=40>'.format(self.category_image.url)
        else:
            return "--"

    def get_count_posts(self):
        """ Получает количество постов """
        count = Post.objects.filter(post_category=self.id).count()
        return count

    show_image.allow_tags = True
    get_count_posts.short_description = "Кол-во постов"


class Post(BaseModel):
    post_title = models.CharField(max_length=255, verbose_name="Заголовок")
    post_category = TreeForeignKey(Category, blank=True)
    post_description = models.CharField(max_length=170, blank=True, verbose_name="META DESC", default="")
    post_text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")
    post_image = models.ImageField(blank=True, default='', upload_to="posts/post_created-%Y-%m-%d", verbose_name="Главное изображение")
    post_active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")

    def __str__(self):
        return "{}".format(self.post_title)

    def show_image(self):
        """ Показывает превью главного изображения в админке """
        if self.post_image:
            return '<img src="{}" width=40>'.format(self.post_image.url)
        else:
            return "--"

    def get_count_comments(self):
        """ Получает количество комментарив поста """
        count = Comment.objects.filter(comment_parent=self.id).count()
        return count

    show_image.allow_tags = True
    show_image.short_description = "Главное изображение"
    get_count_comments.short_description = "Кол-во комментариев"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(BaseModel):
    comment_parent = models.ForeignKey(Post, related_name="comment_parent", verbose_name="Пост коментария")
    comment_text = models.TextField()

    def __str__(self):
        return "Комментарий записи - {}".format(self.comment_parent.post_title)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
