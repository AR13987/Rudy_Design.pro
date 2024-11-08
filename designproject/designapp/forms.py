from django import forms
from django.core.exceptions import ValidationError
import re
class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        label='Имя',
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    last_name = forms.CharField(
        max_length=30,
        label='Фамилия',
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    middle_name = forms.CharField(
        max_length=30,
        label='Отчество',
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    username = forms.CharField(
        max_length=30,
        label='Логин',
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль',
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Повторите пароль',
        required=True,
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True,
        error_messages={'required': 'Вы должны согласиться на обработку персональных данных.'}
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[А-Яа-яЁёs-]+$', first_name):
            raise ValidationError('Имя может содержать только кириллические буквы, пробелы и дефисы.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[А-Яа-яЁёs-]+$', last_name):
            raise ValidationError('Фамилия может содержать только кириллические буквы, пробелы и дефисы.')
        return last_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name')
        if not re.match(r'^[А-Яа-яЁёs-]+$', middle_name):
            raise ValidationError('Отчество может содержать только кириллические буквы, пробелы и дефисы.')
        return middle_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise ValidationError('Логин может содержать только латиницу и дефисы.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Пароли не совпадают.")