from django.contrib import admin
from .models import Racket, Shoes, ShoeAvailability, RacketAvailability, Item

# Register your models here.
admin.site.register(Racket)
admin.site.register(RacketAvailability)
admin.site.register(Shoes)
admin.site.register(ShoeAvailability)
admin.site.register(Item)
