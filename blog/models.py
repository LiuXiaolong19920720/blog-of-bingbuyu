from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=16)

class Tag(models.Model):
    name = models.CharField(max_length=16)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField('标题',max_length=100)
    text = models.TextField('正文')
    content_html = models.TextField('正文-html',default='')
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    
    category = models.ForeignKey(Category,null=True)
    tags = models.ManyToManyField(Tag)
    click_number = models.IntegerField(default=0)  #点击阅读数
    comment_number = models.IntegerField(default=0)  #评论数
    likes = models.PositiveIntegerField(default=0)   #点赞数

    @property
    def total_likes(self):
        return self.likes.count()
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
           
class Comment(models.Model):
    blog = models.ForeignKey(Post,related_name='comments')
    name = models.CharField('输入名称',max_length=16)
    email = models.EmailField('输入邮箱')
    content = models.TextField('输入评论')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    
    

    

