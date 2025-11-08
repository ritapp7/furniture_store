from django.db import models

class User(models.Model):
    first_name = models.CharField(verbose_name='Имя Пользователя', max_length=20)
    last_name = models.CharField("Фамилия", max_length=25)
    email = models.EmailField("Почта")
    phone = models.CharField("Номер", max_length=20)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["first_name", "last_name"]
        indexes = [
            models.Index(fields=["first_name"])
        ]

    def __str__(self):  
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    ST = [
        ("Оформлен", "Оформлен"),
        ("Отправлен", "Отправлен"),
        ("Доставлен", "Доставлен")
    ]

    PM = [
        ("Банковская карта", "Банковская карта"),
        ("При получении", "При получении")
    ]

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField("Статус заказа", max_length=100, choices=ST)
    price = models.DecimalField("Цена", decimal_places=2, max_digits=10)  
    date = models.DateField("Дата заказа")
    delivery_address = models.TextField("Адрес доставки")
    payment_method = models.CharField("Способ оплаты", max_length=20, choices=PM)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        indexes = [
            models.Index(fields=["status"])  
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["id_user", "date"], 
                name="unique_user_order_date"
            ),
        ]

    def __str__(self):
        return f"Заказ #{self.id} - {self.id_user}"

class Category(models.Model):  
    name = models.CharField("Название категории", max_length=20)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField("Название производителя", max_length=50)
    country = models.CharField("Страна", max_length=50)

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Название Товара", max_length=50)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория") 
    id_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", decimal_places=2, max_digits=10)  
    material = models.CharField("Материал", max_length=50)
    weight = models.DecimalField("Вес", decimal_places=2, max_digits=10)  

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

class Position(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField("Количество")
    unit_price = models.DecimalField("Цена за единицу", decimal_places=2, max_digits=10)  

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"
        indexes = [
            models.Index(fields=["id_product"])
        ]

    def __str__(self):
        return f"{self.id_product} x {self.quantity}"
    