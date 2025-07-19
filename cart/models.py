from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField, ForeignKey
from shop.models import Book
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Cart(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)

    def add_item(self, book, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            book=book,
            defaults={'quantity': int(quantity)}
        )

        if not created:
            if int(quantity) >= 1:
                cart_item.quantity += int(quantity)
                cart_item.save()
            else:
                cart_item.quantity -= int(quantity)

    def remove_item(self, book):
        CartItem.objects.filter(cart=self, book=book).delete()

    def get_sum(self):
        return sum(item.get_book_sum() for item in self.items.all())

    def get_items(self):
        return self.items.all()

    def get_count_of_items(self):
        cnt = 0
        for item in self.items.all():
            cnt += item.quantity
        return cnt


class CartItem(models.Model):
    book = ForeignKey(Book, on_delete=models.CASCADE)
    cart = ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(99)])

    def get_book_sum(self):
        return self.book.price * self.quantity
