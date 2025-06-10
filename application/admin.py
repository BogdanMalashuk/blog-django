from django.contrib import admin
from django.contrib.admin import AdminSite
from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.apps import apps


def make_banned(modeladmin, request, queryset):
    queryset.update(status='banned')


make_banned.short_description = 'Mark as banned'


class PostResource(ModelResource):
    class Meta:
        model = Post


class PostAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ('id', 'likes', 'dislikes')
    search_fields = ('author__username', 'id', 'title')
    resource_class = PostResource
    actions = [make_banned]


class PostInline(admin.TabularInline):
    model = Post
    extra = 1


class CustomUserAdmin(BaseUserAdmin):
    inlines = [PostInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
