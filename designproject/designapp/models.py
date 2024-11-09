from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
import re
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    password1 = models.CharField(max_length=128, blank=True, null=True, verbose_name='Пароль')
    password2 = models.CharField(max_length=128, blank=True, null=True, verbose_name='Повтор пароля')
    consent = models.BooleanField(default=False, verbose_name='Я соглашаюсь на обработку моих персональных данных')

    def clean(self):
        super().clean()
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.last_name):
            raise ValidationError('Фамилия должна содержать только кириллические буквы, пробелы и дефисы.')
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.first_name):
            raise ValidationError('Имя должно содержать только кириллические буквы, пробелы и дефисы.')
        if self.middle_name and not re.match(r'^[А-Яа-яЁёs-]*$', self.middle_name):
            raise ValidationError('Отчество должно содержать только кириллические буквы, пробелы и дефисы.')


from django.urls import reverse
class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class FloorPlan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='floor_plans')
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('floorplan-detail', args=[str(self.id)])

    def __str__(self):
        return f"План для {self.project.title}"


class DesignSuggestion(models.Model):
    floor_plan = models.ForeignKey(FloorPlan, on_delete=models.CASCADE, related_name='design_suggestions')
    designer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='design_suggestions')
    suggestion_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('designsuggestion-detail', args=[str(self.id)])

    def __str__(self):
        return f"Предложение по {self.floor_plan}"


# Заявки:
class Application(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)  # Например, 'Принято в работу' или 'Выполнено'

    def get_absolute_url(self):
        return reverse('application-detail', args=[str(self.id)])

    def __str__(self):
        return self.title