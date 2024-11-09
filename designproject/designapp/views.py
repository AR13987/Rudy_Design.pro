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
    return render(request, 'designapp/index.html', context)


from django.views import generic
class ApplicationListView(generic.ListView):
    model = Application


from django.shortcuts import redirect
from .forms import CustomUserCreationForm
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Хранение пароля в зашифрованном виде
            user.save()
            login(request, user)
            return redirect('designapp:index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


from .forms import CustomAuthenticationForm
def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('designapp:index')
            else:
                form.add_error(None, 'Неверный логин или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


from django.contrib.auth import login, authenticate, logout
def logout_user(request):
    logout(request)
    return render(request,'registration/logged_out.html')