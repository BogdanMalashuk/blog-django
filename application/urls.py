from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('main/', views.main, name='main'),
    path('profile/', views.profile, name='profile'),
    path('postdetail/<int:post_id>/', views.postdetail, name='postdetail'),
    path('addpost/', views.addpost, name='addpost'),
    path('deletepost/<int:post_id>/', views.deletepost, name='deletepost'),
    path('editpost/<int:post_id>/', views.editpost, name='editpost'),
    path('delcomment/<int:comment_id>/', views.delcomment, name='delcomment'),
]
