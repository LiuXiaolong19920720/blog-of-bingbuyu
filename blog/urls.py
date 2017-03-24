from django.conf.urls import url,include
from . import views
import ckeditor

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    
    url(r'^like-blog/$', views.like_count_blog, name='like_count_blog'),
    #url(r'ckeditor/',include(ckeditor.urls)),
]