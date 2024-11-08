from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',  # Уникальное имя для доступа к пользователям из группы
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',  # Уникальное имя для доступа к пользователям с разрешениями
        blank=True,
    )

    def __str__(self):
        return self.username


from django.urls import reverse
class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
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
    designer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='design_suggestions')
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