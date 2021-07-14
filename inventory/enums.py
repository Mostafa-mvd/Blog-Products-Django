from django.db import models


class ProductTypes(models.TextChoices):
    JPEG = 'JPEG', "normal quality"
    PSD = 'PSD', 'photoshop file'
    AI = 'AI', 'illustrator'
    TEXT = 'TEXT', 'word file'
    PRINT = 'PRINT', 'print on paper'


class ProductQuality(models.TextChoices):
    GOOD = 'GOOD', 'G'
    MIDDLE = "MIDDLE", "M"
    HIGH = 'HIGH', 'H'
