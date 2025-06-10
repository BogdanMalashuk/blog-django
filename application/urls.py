from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('main/', views.main, name='main'),
    path('main/profile/', views.profile, name='profile'),
    path('main/postdetail/<int:post_id>/', views.postdetail, name='postdetail'),
    path('main/addpost/', views.addpost, name='addpost'),
    path('main/deletepost/<int:post_id>/', views.deletepost, name='deletepost'),
    path('main/editpost/<int:post_id>/', views.editpost, name='editpost'),
    path('main/postdetail/<int:post_id>/delcomment/<int:comment_id>/', views.delcomment, name='delcomment'),
    path('main/postdetail/<int:post_id>/like/', views.like_post, name='like_post'),
    path('main/postdetail/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('main/postdetail/<int:post_id>/reply/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),
]
