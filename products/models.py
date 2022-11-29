from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return 'Category {}'.format(self.category)


class Color(models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return 'Color {}'.format(self.color)


class Brand(models.Model):
    brand = models.CharField(max_length=50)

    def __str__(self):
        return 'Brand {}'.format(self.brand)


class MeasureType(models.Model):
    type = models.CharField(max_length=25)

    def __str__(self):
        return 'Measure type {}'.format(self.type)


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    short_desc = models.CharField(max_length=120, blank=True)
    long_desc = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return '{} from brand {} and category {} has color {}'.format(self.title, self.brand, self.category, self.color)


class ItemMeasures(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.ForeignKey(MeasureType, on_delete=models.CASCADE)
    measure = models.FloatField()
    stock = models.FloatField()
    price = models.FloatField(default=0.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["item", "type", "measure"],
                                    name="One item with a measure can only have a stock.")
        ]

    def __str__(self):
        return 'Item {} with measure {} and stock {}'.format(self.item, self.measure, self.stock)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return 'User {} has item {} in wishlist.'.format(self.user, self.item)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_amount(self):
        total_amount = sum(int(item.item_measure.price) for item in self.items.all())
        return total_amount

    def get_number_of_items(self):
        items = self.items.all().count()
        return items


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item_measure = models.ForeignKey(ItemMeasures, related_name='items', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order {} has item {}.'.format(self.order, self.item_measure.item.title)
