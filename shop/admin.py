from django.contrib import admin

from .models import Car
from .models import Category
from .models import SuperCategory

admin.site.register(Car)
admin.site.register(Category)
admin.site.register(SuperCategory)
