from django.db import models


class Category(models.Model):
    """Модель категорий товаров"""
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """Модель товаров"""
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(to='products.Category', on_delete=models.CASCADE)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class BasketQuerySet(models.QuerySet):
    """Методы для корзины товаров"""
    def total_cost(self):
        return sum(basket.cost() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    """Модель корзины товаров"""
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()  # Добавил методы "total_cost" и "total_quantity"

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def cost(self):
        return self.product.price * self.quantity
