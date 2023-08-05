from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User_info)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(NewsLetterEmail)