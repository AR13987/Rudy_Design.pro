from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
import re
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=False, verbose_name='Фамилия')
    username = models.CharField(max_length=150, unique=True, blank=False, verbose_name='Логин')
    email = models.EmailField(unique=True, blank=False, verbose_name='Электронная почта')
    middle_name = models.CharField(max_length=150, blank=False, verbose_name='Отчество')
    password1 = models.CharField(max_length=128, blank=False, null=True, verbose_name='Пароль')
    password2 = models.CharField(max_length=128, blank=False, null=True, verbose_name='Повтор пароля')
    consent = models.BooleanField(default=False, verbose_name='Я соглашаюсь на обработку моих персональных данных')

    def clean(self):
        super().clean()
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.last_name):
            raise ValidationError('Фамилия должна содержать только кириллические буквы, пробелы и дефисы.')
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.first_name):
            raise ValidationError('Имя должно содержать только кириллические буквы, пробелы и дефисы.')
        if self.middle_name and not re.match(r'^[А-Яа-яЁёs-]*$', self.middle_name):
            raise ValidationError('Отчество должно содержать только кириллические буквы, пробелы и дефисы.')
        if not self.consent:
            raise ValidationError('Необходимо согласие на обработку персональных данных.')


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Заявки:
import os
from django.urls import reverse
class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Новая')  # Например, 'Принято в работу', 'Выполнено', 'Новая'
    photo = models.ImageField(upload_to='photos/', null=True, blank=False)
    comment = models.TextField(null=True, blank=False)
    design_image = models.ImageField(upload_to='designs/', null=True, blank=False)

    @property
    def photo_name(self):
        return os.path.basename(self.photo.name)

    def clean(self):
        super().clean()
        if self.photo:
            if self.photo.size > 2 * 1024 * 1024:  # 2 MB
                raise ValidationError("Размер фото не должен превышать 2 МБ.")
            if not self.photo.name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                raise ValidationError("Недопустимый формат файла. Используйте jpg, jpeg, png, bmp.")

    def get_absolute_url(self):
        return reverse('application-detail', args=[str(self.id)])

    def __str__(self):
        return self.title