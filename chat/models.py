from django.db import models
from myshop.models import CustomUser, Product

class Room(models.Model):
    name = models.CharField(max_length=124, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="get_product_messages", verbose_name="Товар")

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чат"

class Messages(models.Model):
    message = models.TextField(max_length=256, verbose_name="Сообщение")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="get_author_messages", verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Изменено")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="get_room")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("created",)