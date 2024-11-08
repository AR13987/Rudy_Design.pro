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
             )
             messages.success(request, 'Регистрация прошла успешно!')
             return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Неверные учетные данные
            error_message = "Неверное имя пользователя или пароль."
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request, 'registration/login.html')