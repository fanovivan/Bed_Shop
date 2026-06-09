from django.db import models


class Category(models.Model):
    class SlugChoices(models.TextChoices):
        BEDS = "beds", "Кровати"
        SOFAS = "sofas", "Диваны"

    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(
        "Слаг",
        max_length=50,
        unique=True,
        choices=SlugChoices.choices,
    )
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to="products/")
    is_available = models.BooleanField("В наличии", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
