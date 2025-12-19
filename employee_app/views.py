from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
import openpyxl
from openpyxl.styles import Font

from .models import CustomUser
from employee_app.permission_defaults import ROLE_PERMISSIONS
from employee_app.utils import has_permission

def login_view(request):
    if request.user.is_authenticated:
        return redirect('employee_app:users_manager')

    if request.method == 'POST':
        email = request.POST.get('email').lower().strip()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.status == 'active':
                login(request, user)
                return redirect('employee_app:dashboard')
            else:
                messages.error(request, 'Account is inactive.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'employee_app/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('employee_app:login')


@login_required
def users_manager(request):
    if not has_permission(request.user, 'users', 'view'):
        return HttpResponse('Access Denied', status=403)

    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'employee_app/users_manager.html', {'users': users})


@login_required
def create_user(request):
    if not has_permission(request.user, 'users', 'create'):
        return HttpResponse('Access Denied', status=403)

    if request.method == 'POST':
        email = request.POST.get('email').lower().strip()

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('employee_app:users_manager')

        role = request.POST.get('role')

        permissions = ROLE_PERMISSIONS.get(role, {})

        CustomUser.objects.create(
            email=email,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            department=request.POST.get('department') or '',
            role=role,
            status=request.POST.get('status'),
            permissions=permissions,
            password=make_password(request.POST.get('password')),
            is_active=(request.POST.get('status') == 'active')
        )

        messages.success(request, f'User {email} created successfully.')
        return redirect('employee_app:users_manager')

    return redirect('employee_app:users_manager')


@login_required
def edit_user(request, user_id):
    if not has_permission(request.user, 'users', 'edit'):
        return HttpResponse('Access Denied', status=403)

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.phone = request.POST.get('phone')
        user.department = request.POST.get('department') or ''
        user.role = request.POST.get('role')
        user.status = request.POST.get('status')
        user.is_active = (user.status == 'active')

        # reset permissions if role changed
        user.permissions = ROLE_PERMISSIONS.get(user.role, {})
        user.save()

        messages.success(request, 'User updated successfully.')
        return redirect('employee_app:users_manager')

    return render(request, 'employee_app/edit_user.html', {'user': user})


@login_required
def delete_user(request, user_id):
    if not has_permission(request.user, 'users', 'delete'):
        return HttpResponse('Access Denied', status=403)

    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)

        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
        else:
            user.delete()
            messages.success(request, "User deleted successfully.")

    return redirect('employee_app:users_manager')

@login_required
def export_users_excel(request):
    if not has_permission(request.user, 'users', 'export'):
        return HttpResponse('Access Denied', status=403)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="users.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Users"

    columns = ['Full Name', 'Email', 'Phone', 'Department', 'Role', 'Status', 'Date Joined']
    ws.append(columns)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for user in CustomUser.objects.all():
        ws.append([
            user.full_name or '-',
            user.email,
            user.phone or '-',
            user.get_department_display(),
            user.get_role_display(),
            user.get_status_display(),
            user.date_joined.strftime('%Y-%m-%d')
        ])

    wb.save(response)
    return response

@login_required
def dashboard(request):
    if not has_permission(request.user, 'dashboard'):
        return HttpResponse('Access Denied', status=403)
    return render(request, 'employee_app/dashboard.html')





@login_required
def training(request):
    if not has_permission(request.user, 'training'):
        return HttpResponse('Access Denied', status=403)
    return render(request, 'employee_app/training.html')


@login_required
def projects(request):
    if not has_permission(request.user, 'projects'):
        return HttpResponse('Access Denied', status=403)
    return render(request, 'employee_app/projects.html')


@login_required
def profile(request):
    return render(request, 'employee_app/profile.html')

def public_biodata_form(request):
    return render(request, 'employee_app/public_biodata_form.html')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST


@login_required
def app_settings(request):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_sessions = []

    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(request.user.id):
            user_sessions.append(session)

    return render(request, 'employee_app/settings.html', {
        'active_sessions': user_sessions
    })


@login_required
@require_POST
def change_password(request):
    user = request.user

    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if not user.check_password(current_password):
        messages.error(request, "Current password is incorrect")
        return redirect('employee_app:settings')

    if new_password != confirm_password:
        messages.error(request, "Passwords do not match")
        return redirect('employee_app:settings')

    if len(new_password) < 8:
        messages.error(request, "Password must be at least 8 characters")
        return redirect('employee_app:settings')

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)

    messages.success(request, "Password changed successfully")
    return redirect('employee_app:settings')


# @login_required
# @require_POST
# def update_preferences(request):
#     user = request.user
#     user.email_notifications = request.POST.get('email_notifications')
#     user.timezone = request.POST.get('timezone')
#     user.save()

#     messages.success(request, "Preferences updated successfully")
#     return redirect('employee_app:settings')


@login_required
@require_POST
def sign_out_all_devices(request):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())

    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(request.user.id):
            session.delete()

    messages.success(request, "Signed out from all devices")
    return redirect('employee_app:settings')



# Public Form
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import BioDataRequest

def public_biodata_form(request):
    form_data = {}
    errors = {}

    if request.method == 'POST':
        form_data = request.POST

        # Required text fields
        required_text = ['full_name', 'contact_number', 'personal_email', 'experience_type',
                         'technical_skills', 'ssc_school', 'ssc_year', 'ssc_grade',
                         'sslc_school', 'sslc_year', 'sslc_grade', 'ug_degree',
                         'ug_institution', 'ug_year']
        for field in required_text:
            if not request.POST.get(field):
                errors[field] = 'This field is required.'

        # Required files
        required_files = ['photo', 'resume', 'ssc_marksheet', 'sslc_marksheet', 'ug_documents']
        for field in required_files:
            if not request.FILES.get(field):
                errors[field] = 'This file is required.'

        # File size & type
        max_size = 5 * 1024 * 1024
        allowed_types = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
        for key, file in request.FILES.items():
            if file.size > max_size:
                errors[key] = 'File too large (max 5MB)'
            if file.content_type not in allowed_types:
                errors[key] = 'Only PDF, JPG, JPEG, PNG allowed'

        if errors:
            messages.error(request, 'Please correct the errors below.')
        else:
            try:
                work_exp = []
                employers = request.POST.getlist('prev_employer[]')
                designations = request.POST.getlist('prev_designation[]')
                durations = request.POST.getlist('prev_duration[]')
                emails = request.POST.getlist('prev_email[]')
                for i in range(len(employers)):
                    if employers[i].strip():
                        work_exp.append({
                            'employer': employers[i],
                            'designation': designations[i],
                            'duration': durations[i],
                            'email': emails[i],
                        })

                BioDataRequest.objects.create(
                    full_name=request.POST['full_name'],
                    dob=request.POST.get('dob') or None,
                    gender=request.POST.get('gender', ''),
                    marital_status=request.POST.get('marital_status', ''),
                    contact_number=request.POST['contact_number'],
                    emergency_contact=request.POST.get('emergency_contact', ''),
                    personal_email=request.POST['personal_email'],
                    address=request.POST.get('address', ''),
                    aadhar_no=request.POST.get('aadhar_no', ''),
                    pan_no=request.POST.get('pan_no', ''),
                    bank_details=request.POST.get('bank_details', ''),
                    experience_type=request.POST['experience_type'],
                    photo=request.FILES['photo'],
                    resume=request.FILES['resume'],
                    aadhar_card=request.FILES.get('aadhar_card'),
                    pan_card=request.FILES.get('pan_card'),
                    ssc_school=request.POST['ssc_school'],
                    ssc_year=request.POST['ssc_year'],
                    ssc_grade=request.POST['ssc_grade'],
                    ssc_marksheet=request.FILES['ssc_marksheet'],
                    sslc_school=request.POST['sslc_school'],
                    sslc_year=request.POST['sslc_year'],
                    sslc_grade=request.POST['sslc_grade'],
                    sslc_marksheet=request.FILES['sslc_marksheet'],
                    ug_degree=request.POST['ug_degree'],
                    ug_institution=request.POST['ug_institution'],
                    ug_year=request.POST['ug_year'],
                    ug_documents=request.FILES['ug_documents'],
                    pg_degree=request.POST.get('pg_degree', ''),
                    pg_institution=request.POST.get('pg_institution', ''),
                    pg_year=request.POST.get('pg_year') or None,
                    pg_documents=request.FILES.get('pg_documents'),
                    cert_course=request.POST.get('cert_course', ''),
                    cert_institution=request.POST.get('cert_institution', ''),
                    cert_year=request.POST.get('cert_year') or None,
                    cert_document=request.FILES.get('cert_document'),
                    work_experience=work_exp,
                    technical_skills=request.POST['technical_skills'],
                    soft_skills=request.POST.get('soft_skills', ''),
                    reference_name=request.POST.get('reference_name', ''),
                    reference_contact=request.POST.get('reference_contact', ''),
                )

                messages.success(request, 'Bio data submitted successfully! Awaiting HR review.')
                return redirect('employee_app:public_biodata_form')

            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    messages.error(request, 'This email has already been used for a submission.')
                else:
                    messages.error(request, 'An error occurred. Please try again.')

    return render(request, 'employee_app/public_biodata_form.html', {
        'form_data': form_data,
        'errors': errors,
    })

@login_required
def pending_requests(request):
    requests = BioDataRequest.objects.all().order_by('-created_at')
    return render(request, 'employee_app/pending_requests.html', {'requests': requests})

@login_required
def review_biodata_detail(request, pk):
    bio = get_object_or_404(BioDataRequest, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            bio.employee_id = request.POST['employee_id']
            bio.official_email = request.POST['official_email']
            bio.designation = request.POST['designation']
            bio.department = request.POST['department']
            bio.doj = request.POST['doj']
            bio.work_mode = request.POST.get('work_mode', '')
            bio.status = 'approved'
            bio.approved_by = request.user
            bio.save()
            messages.success(request, 'Employee approved successfully!')
            send_mail('Application Approved', 'Your bio data has been approved.', settings.DEFAULT_FROM_EMAIL, [bio.personal_email])

        elif action == 'reject':
            bio.status = 'rejected'
            bio.reject_reason = request.POST['reject_reason']
            bio.save()
            messages.success(request, 'Application rejected.')
            send_mail('Application Rejected', f'Reason: {bio.reject_reason}', settings.DEFAULT_FROM_EMAIL, [bio.personal_email])

        return redirect('employee_app:pending_requests')

    return render(request, 'employee_app/review_biodata_detail.html', {'bio': bio})

@login_required
def biodata_list(request):
    employees = BioDataRequest.objects.filter(status='approved').order_by('-doj')
    return render(request, 'employee_app/biodata.html', {'employees': employees})


# View Bio Data (Read-Only)
@login_required
def view_biodata(request, pk):
    bio = get_object_or_404(BioDataRequest, pk=pk, status='approved')
    return render(request, 'employee_app/view_biodata.html', {'bio': bio})

# Edit Bio Data (HR can edit everything)
@login_required
def edit_biodata(request, pk):
    bio = get_object_or_404(BioDataRequest, pk=pk, status='approved')

    if request.method == 'POST':
        # Update all fields
        bio.full_name = request.POST['full_name']
        bio.dob = request.POST.get('dob') or None
        bio.gender = request.POST.get('gender', '')
        bio.marital_status = request.POST.get('marital_status', '')
        bio.contact_number = request.POST['contact_number']
        bio.emergency_contact = request.POST.get('emergency_contact', '')
        bio.personal_email = request.POST['personal_email']
        bio.address = request.POST.get('address', '')
        bio.aadhar_no = request.POST.get('aadhar_no', '')
        bio.pan_no = request.POST.get('pan_no', '')
        bio.bank_details = request.POST.get('bank_details', '')
        bio.experience_type = request.POST['experience_type']
        bio.technical_skills = request.POST['technical_skills']
        bio.soft_skills = request.POST.get('soft_skills', '')
        bio.reference_name = request.POST.get('reference_name', '')
        bio.reference_contact = request.POST.get('reference_contact', '')

        # HR fields
        bio.employee_id = request.POST['employee_id']
        bio.official_email = request.POST['official_email']
        bio.designation = request.POST['designation']
        bio.department = request.POST['department']
        bio.doj = request.POST['doj']
        bio.work_mode = request.POST.get('work_mode', '')

        bio.save()
        messages.success(request, 'Employee bio data updated successfully!')
        return redirect('employee_app:view_biodata', pk=bio.pk)

    return render(request, 'employee_app/edit_biodata.html', {'bio': bio})