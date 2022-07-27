from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(product)
admin.site.register(user_location)
admin.site.register(product_location)
admin.site.register(history)
