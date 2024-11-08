from django.shortcuts import render

# Create your views here.
from .models import Project, FloorPlan, DesignSuggestion, Application

def index(request):
    # Получаем последние выполненные заявки из базы данных
    applications = Application.objects.all().order_by('-timestamp')[:4]  # Получаем последние 4 заявки
    accepted_count = Application.objects.filter(status='Принято в работу').count()  # Подсчет заявок в статусе "Принято в работу"

    context = {
        'applications': applications,
        'accepted_count': accepted_count,
    }
    return render(request, 'index.html', context)