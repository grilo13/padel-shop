from django.db import models


# Create your models here.
class Racket(models.Model):
    class RacketBrand(models.TextChoices):
        VIBORA = 'Vibora', 'vibora'
        BULLPADEL = 'Bullpadel', 'bullpadel'

    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=30, choices=RacketBrand.choices, default=RacketBrand.VIBORA)
    model = models.IntegerField()

    def __str__(self):
        return "Racket {} from brand {}.".format(self.name, self.brand)


class RacketAvailability(models.Model):
    racket = models.ForeignKey(Racket, on_delete=models.CASCADE)
    weight = models.FloatField()
    available_stock = models.IntegerField()
    price = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["racket", "weight"],
                                    name="A racket with a specific weight can only have a available stock and a price")
        ]

    def __str__(self):
        return "Racket {} weigths {} has a stock of {} and costs {}".format(self.racket.name, self.weight,
                                                                            self.available_stock, self.price)


class Shoes(models.Model):
    class ShoeBrand(models.TextChoices):
        ASICS = 'Asics', 'asics'
        BULLPADEL = 'Bullpadel', 'bullpadel'
        WILSON = 'Wilson', 'wilson'

    name = models.CharField(max_length=120)
    model = models.IntegerField()
    brand = models.CharField(max_length=30, choices=ShoeBrand.choices, default=ShoeBrand.ASICS)

    def __str__(self):
        return "Shoe {} from brand {}".format(self.name, self.brand)


class ShoeAvailability(models.Model):
    shoe = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    size = models.FloatField()
    available_stock = models.IntegerField()
    price = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["shoe", "size"],
                                    name="One shoe object can only have one size for the specific stock")
        ]

    def __str__(self):
        return "Shoe {} size {} has a stock of {} and costs {}".format(self.shoe.name, self.size, self.available_stock,
                                                                       self.price)
