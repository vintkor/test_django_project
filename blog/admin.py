from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from blog.models import Post, Comment, Category


class CommentInline(admin.StackedInline):
    extra = 0
    model = Comment
    suit_classes = 'suit-tab suit-tab-comment'


class PostAdmin(admin.ModelAdmin):
    list_display = ["post_title", "post_category", "post_active", "show_image", "get_count_comments", "created", "updated"]
    list_filter = ["post_active"]
    inlines = [CommentInline]
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-post',),
            'fields': ["post_title", "post_category", "post_image", "post_text", "post_active"]
        }),
    ]

    suit_form_tabs = (('post', 'Пост'), ('comment', 'Комментарии'))


class CommentAdmin(admin.ModelAdmin):
    list_display = ["comment_parent", "created", "updated"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        "tree_actions", "indented_title", "get_count_posts", "show_image", "created", "updated"
    ),
    list_display_links=(
        'indented_title',
    ),
)
