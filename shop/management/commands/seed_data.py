import io
import re
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from shop.models import Category, Product

PRODUCTS_DATA = [
    {
        "category": "beds",
        "name": "Кровать «Комфорт»",
        "description": (
            "Двуспальная кровать с мягким изголовьем и ортопедическим основанием. "
            "Каркас из массива бука, обивка велюр."
        ),
        "price": Decimal("45900.00"),
        "color": (45, 90, 61),
    },
    {
        "category": "beds",
        "name": "Кровать «Минимал»",
        "description": (
            "Лаконичная платформенная кровать без изголовья. "
            "Идеальна для современных интерьеров в скандинавском стиле."
        ),
        "price": Decimal("32500.00"),
        "color": (196, 165, 116),
    },
    {
        "category": "beds",
        "name": "Кровать «Классика»",
        "description": (
            "Кровать с резным изголовьем в классическом стиле. "
            "Натуральное дерево, ручная обработка деталей."
        ),
        "price": Decimal("67800.00"),
        "color": (139, 90, 43),
    },
    {
        "category": "beds",
        "name": "Кровать «Лофт»",
        "description": (
            "Металлический каркас с деревянными вставками. "
            "Индустриальный дизайн для городских квартир."
        ),
        "price": Decimal("38900.00"),
        "color": (80, 80, 80),
    },
    {
        "category": "sofas",
        "name": "Диван «Уют»",
        "description": (
            "Трёхместный раскладной диван с ящиком для белья. "
            "Пружинный блок, съёмные подушки, ткань микрофибра."
        ),
        "price": Decimal("52900.00"),
        "color": (70, 130, 180),
    },
    {
        "category": "sofas",
        "name": "Диван «Модерн»",
        "description": (
            "Угловой диван с механизмом трансформации «дельфин». "
            "Просторное спальное место 160×200 см."
        ),
        "price": Decimal("78900.00"),
        "color": (100, 149, 237),
    },
    {
        "category": "sofas",
        "name": "Диван «Сканди»",
        "description": (
            "Компактный двухместный диван в скандинавском стиле. "
            "Светлые тона, натуральные материалы, высокие ножки."
        ),
        "price": Decimal("41500.00"),
        "color": (210, 180, 140),
    },
    {
        "category": "sofas",
        "name": "Диван «Премиум»",
        "description": (
            "Прямой диван премиум-класса с кожаной обивкой. "
            "Наполнитель пенополиуретан высокой плотности."
        ),
        "price": Decimal("125000.00"),
        "color": (50, 50, 50),
    },
]

CATEGORIES_DATA = [
    {
        "slug": "beds",
        "name": "Кровати",
        "description": (
            "Двуспальные и односпальные кровати с ортопедическими основаниями."
        ),
    },
    {
        "slug": "sofas",
        "name": "Диваны",
        "description": "Прямые, угловые и раскладные диваны для гостиной.",
    },
]


def generate_product_image(name, color, category_name):
    width, height = 600, 400
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)

    lighter = tuple(min(c + 40, 255) for c in color)
    draw.rectangle([50, 80, width - 50, height - 80], fill=lighter)

    emoji = "🛏" if "Кроват" in category_name else "🛋"
    try:
        font = ImageFont.truetype("arial.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        small_font = font

    draw.text(
        (width // 2, height // 2 - 30),
        emoji,
        fill=(255, 255, 255),
        anchor="mm",
        font=font,
    )

    short_name = name.replace("«", "").replace("»", "")[:30]
    draw.text(
        (width // 2, height // 2 + 30),
        short_name,
        fill=(255, 255, 255),
        anchor="mm",
        font=small_font,
    )

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    return buffer


class Command(BaseCommand):
    help = "Заполняет базу данных категориями и товарами с изображениями"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить существующие данные перед заполнением",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Существующие данные удалены.")

        categories = {}
        for cat_data in CATEGORIES_DATA:
            category, created = Category.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={
                    "name": cat_data["name"],
                    "description": cat_data["description"],
                },
            )
            categories[cat_data["slug"]] = category
            status = "создана" if created else "уже существует"
            self.stdout.write(f"Категория «{category.name}» — {status}")

        for product_data in PRODUCTS_DATA:
            category = categories[product_data["category"]]
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "category": category,
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "is_available": True,
                },
            )

            if created or not product.image:
                image_buffer = generate_product_image(
                    product_data["name"],
                    product_data["color"],
                    category.name,
                )
                safe_name = re.sub(
                    r"[^\w\-]", "", product.name.replace(" ", "-").lower()
                )
                filename = f"{safe_name}-{product.id}.jpg"
                product.image.save(
                    filename, ContentFile(image_buffer.read()), save=True
                )

            status = "создан" if created else "обновлён"
            self.stdout.write(f"Товар «{product.name}» — {status}")

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))
