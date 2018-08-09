from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Image, Post, CustomData, City, District, Category, Window, Material, State, Currency, \
    TreeCategory


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomData.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.custom.save()


class ImageInline(admin.StackedInline):
    model = Image


from multiupload.admin import MultiUploadAdmin
class MyModelAdmin(MultiUploadAdmin):
    # default value of all parameters:
    change_form_template = 'multiupload/change_form.html'
    change_list_template = 'multiupload/change_list.html'
    multiupload_template = 'multiupload/upload.html'
    # if true, enable multiupload on list screen
    # generaly used when the model is the uploaded element
    multiupload_list = True
    # if true enable multiupload on edit screen
    # generaly used when the model is a container for uploaded files
    # eg: gallery
    # can upload files direct inside a gallery.
    multiupload_form = True
    # max allowed filesize for uploads in bytes
    multiupload_maxfilesize = 3 * 2 ** 20 # 3 Mb
    # min allowed filesize for uploads in bytes
    multiupload_minfilesize = 0
    # tuple with mimetype accepted
    multiupload_acceptedformats = ( "image/jpeg",
                                    "image/pjpeg",
                                    "image/png",)

    def process_uploaded_file(self, uploaded, object, request):
        '''
        Process uploaded file
        Parameters:
            uploaded: File that was uploaded
            object: parent object where multiupload is
            request: request Object
        Must return a dict with:
        return {
            'url': 'url to download the file',
            'thumbnail_url': 'some url for an image_thumbnail or icon',
            'id': 'id of instance created in this method',
            'name': 'the name of created file',

            # optionals
            "size": "filesize",
            "type": "file content type",
            "delete_type": "POST",
            "error" = 'Error message or jQueryFileUpload Error code'
        }
        '''
        # example:
        title = kwargs.get('title', [''])[0] or uploaded.name
        f = self.model(upload=uploaded, title=title)
        f.save()
        return {
            'url': f.image_thumb(),
            'thumbnail_url': f.image_thumb(),
            'id': f.id,
            'name': f.title
        }

    def delete_file(self, pk, request):
        '''
        Function to delete a file.
        '''
        # This is the default implementation.
        obj = get_object_or_404(self.queryset(request), pk=pk)
        obj.delete()

class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]
    list_display = ('id', 'category_tree', 'is_top', 'title', 'price', 'currency_type', 'created', 'district', 'owner')
    list_select_related = ('currency_type', 'category_tree')
    list_filter = (
        'closed', 'owner', 'district', 'category_tree'
    )

    # list_editable = ('is_top', 'title', 'price', 'currency_type', 'category_tree')

    list_per_page = 30

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.images.create(image=afile)


class CityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Category)
# admin.site.register(Living_space)
admin.site.register(Window)
admin.site.register(Material)
admin.site.register(State)
admin.site.register(Currency)
admin.site.register(TreeCategory)


class CustomDataInline(admin.StackedInline):
    model = CustomData
    can_delete = False
    extra = 1


class UserAdmin(BaseUserAdmin):
    inlines = (CustomDataInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.site_header = 'Первый Риэлторский Центр'
