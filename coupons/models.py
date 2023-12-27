from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Coupon(models.Model):
    """Модель купона."""
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Код',
    )
    valid_from = models.DateTimeField(
        verbose_name='Начало срока',
    )
    valid_to = models.DateTimeField(
        verbose_name='Конец срока',
    )
    discount = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text='Процентное значение (0 до 100)',
        verbose_name='Скидка',
    )
    active = models.BooleanField(
        verbose_name='Статус активности',
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
