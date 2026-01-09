
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
    path('training/add/', views.add_trainee, name='add_trainee'), 
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


      
    path('batch-form/', views.batch_form, name='create_batch'),
    path('batch-details/', views.batch_details, name='batch_details'),
    path('batch-edit/', views.edit_batch, name='edit_batch'),
    path('session-form/', views.session_form, name='create_session'),
    path('session-edit/', views.edit_session, name='edit_session'),
    path('session-details/', views.session_details, name='session_details'),
    path('assignment-form/', views.assignment_form, name='create_assignment'),
    path('assignment-edit/', views.edit_assignment, name='edit_assignment'),
    path('assignment-details/', views.assignment_details, name='assignment_details'),

    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/profile/', views.my_profile, name='my_profile'),
    path('employee/profile/edit/', views.edit_my_profile, name='edit_my_profile'),

    path('biodata/delete-pending/<int:pk>/', views.delete_pending_request, name='delete_pending_request'),
path('biodata/delete-approved/<int:pk>/', views.delete_approved_employee, name='delete_approved_employee'),
]
