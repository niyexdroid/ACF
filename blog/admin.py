from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Post)

admin.site.register(Category)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['commentor_name', 'comment_post', 'content']
    @admin.display()
    def comment_post(self, obj):
        return obj.post.title
    
@admin.register(Video)
class VIdeoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ['url']