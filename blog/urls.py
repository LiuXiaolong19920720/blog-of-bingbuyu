from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),   
    url(r'^like-blog/$', views.like_count_blog, name='like_count_blog'),
    url(r'^delete-blog/(?P<pk>\w+)/$', views.delete_blog, name='delete_blog'),
    url(r'^opencv',views.opencv,name='opencv'),
    url(r'^neural-network',views.nn,name='neural-network'),
    url(r'^me',views.me,name='me'),
]
