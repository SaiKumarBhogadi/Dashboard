from django.urls import path
from employee_app.views import (
    login_view, logout_view, users_manager,
    create_user, edit_user, delete_user,
    export_users_excel, dashboard
)
from . import views

app_name = 'employee_app'

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('users/', users_manager, name='users_manager'),
    path('users/create/', create_user, name='create_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/export/', export_users_excel, name='export_users_excel'),

    path('dashboard/', dashboard, name='dashboard'),

    
    path('training/', views.training, name='training'),
    path('projects/', views.projects, name='projects'),
    path('profile/', views.profile, name='profile'),

    path('public_biodata_form/', views.public_biodata_form, name='public_biodata_form'),
    path('biodata/public/', views.public_biodata_form, name='public_biodata_form'),
    path('biodata/requests/', views.pending_requests, name='pending_requests'),
    path('biodata/review/<int:pk>/', views.review_biodata_detail, name='review_biodata_detail'),
    path('biodata/employees/', views.biodata_list, name='biodata_list'),
    path('biodata/view/<int:pk>/', views.view_biodata, name='view_biodata'),
    path('biodata/edit/<int:pk>/', views.edit_biodata, name='edit_biodata'),
    path('biodata/delete/<int:pk>/', views.delete_biodata, name='delete_biodata'),
    path('biodata/export/', views.export_biodata_excel, name='export_biodata_excel'),

    path('settings/', views.app_settings, name='settings'),
    path('api/settings/change_password/', views.change_password, name='change_password'),
    path('api/settings/signout_all/', views.sign_out_all_devices, name='signout_all'),

    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('notifications/all/', views.notifications_all, name='notifications_all'),
]
