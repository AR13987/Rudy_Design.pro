from django.shortcuts import render

# Create your views here.
from .models import Project, FloorPlan, DesignSuggestion, Application


def index(request):
    # Получаем последние выполненные заявки из базы данных
    applications = Application.objects.filter(status='Выполнено').order_by('-timestamp')[:4]  # Получаем последние 4 выполненные заявки
    accepted_count = Application.objects.filter(status='Принято в работу').count()  # Подсчет заявок в статусе "Принято в работу"

    context = {
        'applications': applications,
        'accepted_count': accepted_count,
    }
    return render(request, 'designapp/index.html', context)


from django.views import generic
class ApplicationListView(generic.ListView):
    model = Application
    template_name = 'designapp/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        queryset = Application.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')  # Получаем статус из GET-параметров
        if status:
            queryset = queryset.filter(status=status)  # Фильтруем по статусу
        return queryset


from .forms import ApplicationForm
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)  # Не сохраняем сразу
            application.user = request.user  # Устанавливаем текущего пользователя
            application.save()
            return redirect('designapp:profile')
    else:
        form = ApplicationForm()

    return render(request, 'designapp/application_create.html', {'form': form})


from django.shortcuts import get_object_or_404
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        application.delete()
        return redirect('designapp:profile')
    return render(request, 'designapp/confirm_delete.html', {'application': application})


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


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
class AdminProfileView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'designapp/admin_profile.html'

    def test_func(self):
        return self.request.user.is_superuser  # Проверка, является ли пользователь администратором



from django.contrib import messages
from .models import Category
from django.views import View
class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'designapp/manage_categories.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def test_func(self):
        return self.request.user.is_superuser


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request):
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, 'Категория добавлена!')
        else:
            messages.error(request, 'Введите название категории.')
        return redirect('designapp:admin-category-list')

    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete()  # Удаление категории
            messages.success(request, 'Категория удалена!')
        except Category.DoesNotExist:
            messages.error(request, 'Категория не найдена.')
        return redirect('designapp:admin-category-list')

    def test_func(self):
        return self.request.user.is_superuser