from django.db import models


# Create your models here.
class Racket(models.Model):
    class RacketBrand(models.TextChoices):
        VIBORA = 'Vibora', 'vibora'
        BULLPADEL = 'Bullpadel', 'bullpadel'
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=30, choices=RacketBrand.choices, default=RacketBrand.VIBORA)
    model = models.IntegerField()
    availability = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return "Racket {} from brand {} costs {}".format(self.name, self.brand, self.price)
