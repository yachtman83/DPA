from django import forms
from .models import *


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'last_name', 'first_name', 'email']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Эл.почта',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'can_edit_courses']


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'subscriptions', 'photo']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'subscriptions': 'Подписки',
            'photo': 'Фото',
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class CourseForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('students', 'Студентам'),
        ('ege', 'Подготовка к ЕГЭ'),
    ]

    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)
    image = forms.ImageField(required=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'image']


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data