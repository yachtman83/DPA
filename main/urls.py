from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.user_profile, name='user_profile'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('students_courses', views.students_courses, name='students_courses'),
    path('ege_courses', views.ege_courses, name='ege_courses'),
    path('course_edit', views.course_edit, name='course_edit'),
    path('course_delete/<int:course_id>', views.course_delete, name='course_delete'),
    path('course_add', views.course_add, name='course_add'),
    path('course_subscription/<int:course_id>/', views.course_subscription, name='course_subscription'),
    path('my_courses', views.my_courses, name='my_courses'),
    path('course_details/<int:course_id>', views.course_details, name='course_details'),

    path('course/<int:course_id>/delete/', views.course_delete_from_my_list, name='course_delete_from_my_list'),

    path('course_edit/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('course_edit/<int:course_id>/current_course_edit/', views.current_course_edit, name='current_course_edit'),

    path('non_editable_users', views.non_editable_users, name='non_editable_users'),
    path('edit_user/<int:user_id>', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('user_subscriptions/<int:user_id>', views.user_subscriptions, name='user_subscriptions'),
    path('create_user', views.create_user, name='create_user'),
    path('profile/edit_profile', views.user_profile_edit, name='user_profile_edit'),
    path('course/<int:course_id>/lesson/', views.course_lesson, name='course_lesson'),
    path('lesson/edit/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)