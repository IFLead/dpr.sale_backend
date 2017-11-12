import os
from django import template
from django.core.files.storage import default_storage

from Realtor.settings import BASE_DIR, PROJECT_DIR

register = template.Library()


@register.filter(name='file_exists')
def file_exists(filepath):
    return filepath is not None and default_storage.exists(os.path.join(BASE_DIR, filepath[1:]))
