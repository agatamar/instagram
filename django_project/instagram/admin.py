from django.contrib import admin
from instagram.models import Photo, Comment,Preference
# Register your models here.

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    exclude = ['creation_date', ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    exclude = ['creation_date', ]

@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    exclude = ['date', ]

