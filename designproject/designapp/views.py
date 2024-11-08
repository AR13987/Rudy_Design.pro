from django.shortcuts import render

# Create your views here.
from .models import Project, FloorPlan, DesignSuggestion, Application, CustomUser


def index(request):
    # Получаем последние выполненные заявки из базы данных
    applications = Application.objects.all().order_by('-timestamp')[:4]  # Получаем последние 4 заявки
    accepted_count = Application.objects.filter(status='Принято в работу').count()  # Подсчет заявок в статусе "Принято в работу"

    context = {
        'applications': applications,
        'accepted_count': accepted_count,
    }
    return render(request, 'index.html', context)



from django.views import generic
class ApplicationListView(generic.ListView):
    model = Application



from django.shortcuts import redirect
from .forms import RegistrationForm
from django.contrib import messages
from .models import CustomUser
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
             user = CustomUser.objects.create_user(
                 username=form.cleaned_data['username'],
                 email=form.cleaned_data['email'],
                 password=form.cleaned_data['password'],
                 first_name=form.cleaned_data['first_name'],
                 last_name=form.cleaned_data['last_name'],
                 middle_name=form.cleaned_data['middle_name'],
             )
             messages.success(request, 'Регистрация прошла успешно!')
             return redirect('register')  # перенаправление на страницу регистрации или входа
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})