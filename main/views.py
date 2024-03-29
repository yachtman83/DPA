from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Subscription, UserProfile
from django.contrib import messages
from django.db.models import Q
from .models import Course, Lesson
from datetime import date as dt, datetime


@login_required
def user_profile(request):
    user = request.user
    subscriptions = user.subscriptions.all()

    context = {
        'user': user,
        'subscriptions': subscriptions
    }

    return render(request, 'user_profile.html', context)

@login_required
def user_profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileEditForm(instance=user)

    context = {
        'form': form
    }

    return render(request, 'user_profile_edit.html', context)

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def students_courses(request):
    courses = Course.objects.filter(category='students')
    return render(request, 'main/students_courses.html', {'courses': courses})


def ege_courses(request):
    courses = Course.objects.filter(category='ege')
    return render(request, 'main/ege_courses.html', {'courses': courses})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.can_edit_courses:
                    return redirect('course_edit')
                else:
                    return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def index(request):
    return render(request, 'main/main.html')


def about(request):
    return render(request, 'main/about.html')


def course_edit(request, course_id=None):
    # Проверяем, является ли пользователь аутентифицированным и имеет права на редактирование курсов
    if request.user.is_authenticated and request.user.can_edit_courses:
        courses = Course.objects.all()  # Получаем все курсы
        if course_id is not None:
            # Редактирование существующего курса
            course = get_object_or_404(Course, id=course_id)
        else:
            # Добавление нового курса
            course = None

        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('home')  # Или другую страницу после успешного сохранения
        else:
            form = CourseForm(instance=course)

        return render(request, 'main/course_edit.html', {'form': form, 'course_id': course_id, 'courses': courses})
    else:
        return redirect('home')  # Или обработайте ошибку соответствующим образом


# def course_delete(request, course_id):
#     if request.user.is_authenticated and request.user.can_edit_courses:
#         course = get_object_or_404(Course, id=course_id)
#         course.delete()
#         return redirect('home')  # Или другую страницу после успешного удаления
#     else:
#         return redirect('home')  # Или обработайте ошибку соответствующим образом

def course_delete(request, course_id):
    user_profile = request.user

    if user_profile.is_authenticated and user_profile.can_edit_courses:
        course = Course.objects.get(id=course_id)
        course.delete()
        messages.info(request, 'Удаление прошло успешно')
    else:
        messages.error(request, 'Ошибка при удалении курса')

    return redirect(request.META.get('HTTP_REFERER'))

def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_edit')
    else:
        form = CourseForm()

    return render(request, 'main/course_add.html', {'form': form})


def current_course_edit(request, course_id):
    user_profile = request.user

    if user_profile.is_authenticated and user_profile.can_edit_courses:
        course = get_object_or_404(Course, id=course_id)
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                messages.success(request, 'Курс успешно отредактирован')
                return redirect('course_edit')  # Или другую страницу после успешного редактирования
        else:
            form = CourseForm(instance=course)

        return render(request, 'main/current_course_edit.html', {'form': form})


def course_subscription(request, course_id):
    if request.method == 'GET':
        course = Course.objects.get(id=course_id)
        # Проверяем, что пользователь аутентифицирован
        if request.user.is_authenticated:
            # Создаем объект Subscription и связываем его с текущим пользователем и курсом
            subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)
            if created:
                # Курс успешно добавлен
                messages.success(request, 'Курс был успешно добавлен в "Мои курсы"')
            else:
                # Пользователь уже имеет этот курс в своих курсах
                messages.info(request, 'Этот курс уже есть в "Мои курсы"')

    # Возвращаем пользователя на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER'))


def my_courses(request):
    if request.user.is_authenticated:
        user = request.user
        courses = user.subscriptions.all()
        return render(request, 'main/my_courses.html', {'courses': courses})
    else:
        messages.warning(request, 'Вам необходимо войти или пройти регистрацию')
        return redirect(request.META.get('HTTP_REFERER'))


def course_details(request, course_id):
    course = Course.objects.get(id=course_id)
    current_date = dt.today()
    current_time = datetime.now().time()
    lessons = Lesson.objects.filter(
        Q(date__gt=current_date) | (Q(date=current_date) & Q(time__gt=current_time)),
        course=course
    ).order_by('date', 'time')

    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, 'main/course_details.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def course_delete_from_my_list(request, course_id):
    user_profile = request.user
    course = Course.objects.get(id=course_id)
    user_profile.subscriptions.remove(course)
    messages.info(request, 'Удаление прошло успешно')
    return redirect(request.META.get('HTTP_REFERER'))


def non_editable_users(request):
    users = UserProfile.objects.filter(can_edit_courses=False)
    context = {'users': users}
    return render(request, 'non_editable_users.html', context)


def user_subscriptions(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    subscriptions = user.subscriptions.all()
    context = {'user': user, 'subscriptions': subscriptions}
    return render(request, 'user_subscriptions.html', context)


def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            messages.info(request, 'Смена пароля выполнена')
            return redirect('non_editable_users')
    else:
        form = ChangePasswordForm()

    context = {'user': user, 'form': form}
    return render(request, 'edit_user.html', context)


def create_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            # Добавьте сообщение об успешном создании пользователя
            return redirect('non_editable_users')
    else:
        form = UserProfileForm()
    context = {'form': form}
    return render(request, 'create_user.html', context)


def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.info(request, 'Удаление прошло успешно')
        return redirect('non_editable_users')
    context = {'user': user}
    return render(request, 'delete_user.html', context)


def course_lesson(request, course_id):
    course = Course.objects.get(id=course_id)

    # Фильтруем занятия по дате и времени
    current_date = dt.today()
    current_time = datetime.now().time()
    lessons = Lesson.objects.filter(
        Q(date__gt=current_date) | (Q(date=current_date) & Q(time__gt=current_time)),
        course=course
    ).order_by('date', 'time')

    context = {
        'course': course,
        'lessons': lessons
    }

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        assignment = request.FILES.get('assignment')

        lesson = Lesson(course=course, date=date, time=time, assignment=assignment)
        lesson.save()
        messages.info(request, 'Занятие добавлено')
        return redirect('course_lesson', course_id=course_id)

    return render(request, 'course_lesson.html', context)


def edit_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            date = request.POST.get('date')
            time = request.POST.get('time')
            assignment = request.FILES.get('assignment')

            lesson.date = date
            lesson.time = time
            if assignment:
                lesson.assignment = assignment
            messages.info(request, 'Изменения сохранены')
            lesson.save()

        elif action == 'delete':
            lesson.delete()
            messages.info(request, 'Удаление прошло успешно')
            return redirect('course_lesson', course_id=lesson.course.id)

    context = {
        'lesson': lesson,
    }

    return render(request, 'edit_lesson.html', context)