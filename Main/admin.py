from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Image, Post, CustomData, City, District, Category, Living_space, Window, Material, State


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomData.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.custom.save()


class ImageInline(admin.StackedInline):
    model = Image


class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]


admin.site.register(Post, PostAdmin)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Category)
admin.site.register(Living_space)
admin.site.register(Window)
admin.site.register(Material)
admin.site.register(State)


class CustomDataInline(admin.StackedInline):
    model = CustomData
    can_delete = False
    extra = 1


class UserAdmin(BaseUserAdmin):
    inlines = (CustomDataInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.site_header = 'Первый Риэлторский Центр'
