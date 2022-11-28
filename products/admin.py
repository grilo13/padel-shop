from django.contrib import admin
from .models import Racket, Shoes, ShoeAvailability, RacketAvailability, Item, ItemMeasures, Color, Category, Brand

# Register your models here.
admin.site.register(Racket)
admin.site.register(RacketAvailability)
admin.site.register(Shoes)
admin.site.register(ShoeAvailability)
admin.site.register(Item)
admin.site.register(ItemMeasures)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Category)
