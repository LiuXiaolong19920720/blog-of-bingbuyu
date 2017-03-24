from django.contrib import admin
from .models import Post,Category, Tag,Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','published_date')
    list_filter = ('author','created_date', 'published_date')
    search_fields = ('title', 'text')
    date_hierarchy = 'published_date'
    ordering = ['-published_date']
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','blog','created')
    list_filter = ('active','created','blog')
    search_fields = ('content','name','email')
    ordering = ['-created']
    
admin.site.register(Post,PostAdmin)
admin.site.register([Category, Tag])
admin.site.register(Comment, CommentAdmin)