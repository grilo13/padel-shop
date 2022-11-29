from django.contrib import admin
from .models import Item, ItemMeasures, Color, Category, Brand, \
    MeasureType, Wishlist

# Register your models here.
admin.site.register(Item)
admin.site.register(ItemMeasures)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(MeasureType)
admin.site.register(Wishlist)
