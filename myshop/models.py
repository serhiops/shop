from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from djmoney.models.fields import MoneyField
from django.utils.text import slugify
from .additionally.func import generate_code

class CustomUser(AbstractUser):
    code = models.IntegerField(verbose_name="Код", blank=True, null=True)
    is_salesman = models.BooleanField(default = False, verbose_name="Продавец")
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)
    number_of_phone =  models.CharField(max_length=13,verbose_name="Номер телефона", blank=True, null=True)
    city = models.CharField(max_length=64, verbose_name="Населенный пункт", blank=True, null=True)
    company = models.CharField(max_length=64, verbose_name="Компания", default="company name", blank=True, null=True)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('-date_joined',)

    def __str__(self):
        return f"{self.username} is salesman: {self.is_salesman} is active: {self.is_active}"

class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название")
    description = models.CharField(max_length=128,verbose_name="Описание")
    slug = models.SlugField(max_length=64, verbose_name="URL",unique=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse("myshop:by_category", kwargs={"cat_slug":self.slug})

    def __str__(self):
        return self.name

class Coments(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="get_author", verbose_name="Автор")
    text = models.TextField(max_length=1024, verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Изменено")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="get_prd", verbose_name="Товар")
    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.author} : {self.text}"

class Photo(models.Model):
   image = models.ImageField(upload_to="images/products/%Y/%m/%d", verbose_name="Изображение")
   product = models.ForeignKey("Product",on_delete=models.CASCADE, related_name='photos')

class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='UAH', verbose_name="Цена")
    salesman = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="get_salseman", verbose_name="Продавец")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Изменен")
    slug = models.SlugField(max_length=64, verbose_name="URL", unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name = "get_category", verbose_name="Категория")
    views = models.ManyToManyField("Ip", related_name="post_views", blank=True)
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.name} : {self.price}"
    
    def total(self):
        return self.views.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if Product.objects.filter(slug = self.slug):
            self.slug += str(generate_code())
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("myshop:detail", kwargs={"prod_pk":self.pk,"prod_slug":self.slug})

    def get_absolute_url_toApi(self):
        return reverse('myshop:detail-product-api', kwargs={'pk':self.pk})

    def get_absolute_url_detail_statistic(self):
        return reverse("myshop:detail_statistic", kwargs={"slug_pr":self.slug})

    def get_absolute_url_delete_product(self):
        return reverse("myshop:delete_product", kwargs={"slug_pr":self.slug})

    def get_absolute_url_change_product(self):
        return reverse("myshop:change_product", kwargs={"slug_pr":self.slug})

    def get_absolute_url_setActive_product(self):
        return reverse("myshop:set_active", kwargs={"slug_prd":self.slug})

    def get_absolute_url_add_to_favoriteProducts(self):
        return reverse("myshop:add_to_favoriteProducts", kwargs={"pk":self.pk})
    
class PostOfices(models.Model):
    name = models.CharField(max_length=64 , verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    def __str__(self):
        return self.name

class FavoriteProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="get_product", verbose_name="Товар")
    added  = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="get_fp")
    salesman = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="get_salesm")
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("-added",)

    def __str__(self):
        return f"{self.product} : {self.user}"

    def get_absolute_url(self):
        return reverse("myshop:delete_fav_pr", kwargs={"pk_fp":self.pk})

    def get_absolute_url_to_Ordering(self):
        return reverse("myshop:ordering", kwargs={"pk_sal":self.salesman.pk, "slug_prod":self.product.slug})

class Ip(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Ordering(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="get_user", verbose_name="Покупатель")
    salesman = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="get_sal", verbose_name="Продавец")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="get_pr", verbose_name="Товар")
    post_office = models.ForeignKey(PostOfices, on_delete=models.DO_NOTHING, related_name="get_pf", verbose_name="Почтовое отделение")
    number = models.PositiveIntegerField(verbose_name="Количество", default=1)
    is_done = models.BooleanField(default=False, verbose_name="Выполнено")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")
    is_take = models.BooleanField(default=False, verbose_name="Принято")
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.salesman}->{self.user}, product : {self.product}"

    def get_absolute_url_to_product(self):
        return reverse("myshop:detail", kwargs={"prod_pk":self.product.pk, "prod_slug":self.product.slug})

    def get_absolute_url_setDone(self):
        return reverse("myshop:set_done", kwargs={"pk_ord":self.pk})

class Mark(models.Model):
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="get_p", verbose_name="Товар")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="get_us", verbose_name="Пользователь")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Изменен")

    class Meta:
        verbose_name = "Оценка"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user} : like:{self.like}, dislike:{self.dislike}"

class Rating(models.Model):
    
    VERY_BAD = 1
    BAD = 2
    FINE = 3
    WELL = 4
    GREAT = 5
    ZERO = 0

    STATUS_CHOICES = (
        (ZERO, "ZERO"),
        (VERY_BAD,"VERY_BAD"),
        (BAD,"BAD"),
        (FINE,"FINE"),
        (WELL,"WELL"),
        (GREAT,"GREAT"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="get_userr", verbose_name="Пользователь")
    rating = models.IntegerField(default=ZERO, choices=STATUS_CHOICES)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="get_prod", verbose_name="Товар")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Изменен")
