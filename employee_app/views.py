# --- Static Template Preview Views ---
from django.views.generic import TemplateView



def batch_form(request):
    return render(request, 'employee_app/batch_form.html')

def session_form(request):
    return render(request, 'employee_app/session_form.html')

def assignment_form(request):
    return render(request, 'employee_app/assignment_form.html')

def batch_details(request):
    return render(request, 'employee_app/batch_details.html')

def session_details(request):
    return render(request, 'employee_app/session_details.html')

def assignment_details(request):
    return render(request, 'employee_app/assignment_details.html')

def edit_batch(request):
    return render(request, 'employee_app/edit_batch.html')

def edit_session(request):
    return render(request, 'employee_app/edit_session.html')

def edit_assignment(request):
    return render(request, 'employee_app/edit_assignment.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
import openpyxl
from openpyxl.styles import Font
from django.urls import reverse
from .utils import create_notification  

from .models import CustomUser
from employee_app.permission_defaults import ROLE_PERMISSIONS
from employee_app.utils import create_notification, has_permission

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

        new_user = CustomUser.objects.create(
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

        # === NOTIFICATION: New user created → notify admin & super_admin ===
        for notifier in CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True):
            link = reverse('employee_app:edit_user', args=[new_user.id])
            create_notification(
                recipient=notifier,
                ntype='user_created',
                title='New User Created',
                message=f"User {new_user.email} ({new_user.get_role_display()}) was created by {request.user.get_full_name() or request.user.email}.",
                link=request.build_absolute_uri(link)
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

        # === NOTIFICATION: User edited → notify ONLY the edited user ===
        create_notification(
            recipient=user,
            ntype='user_updated',
            title='Your Profile Was Updated',
            message=f"Your account details were updated by {request.user.get_full_name() or request.user.email}.",
            link=request.build_absolute_uri(reverse('employee_app:profile'))
        )

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
            deleted_email = user.email
            deleted_role = user.get_role_display()
            user.delete()

            # === NOTIFICATION: User deleted → notify admin & super_admin ===
            for notifier in CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True):
                create_notification(
                    recipient=notifier,
                    ntype='user_deleted',
                    title='User Deleted',
                    message=f"User {deleted_email} ({deleted_role}) was deleted by {request.user.get_full_name() or request.user.email}.",
                )

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
    if not has_permission(request.user, 'dashboard', 'view'):
        return HttpResponse('Access Denied', status=403)
    return render(request, 'employee_app/dashboard.html')






@login_required
def training(request):
    if not has_permission(request.user, 'training', 'view'):
        return HttpResponse('Access Denied', status=403)
    return render(request, 'employee_app/training.html')

@login_required
def add_trainee(request):
    if not has_permission(request.user, 'training', 'create'):
        return HttpResponse('Access Denied', status=403)
    return render(request, 'employee_app/add_trainee.html')



@login_required
def projects(request):
    if not has_permission(request.user, 'projects', 'view'):
        return HttpResponse('Access Denied', status=403)
    return render(request, 'employee_app/projects.html')



@login_required
def profile(request):
    return render(request, 'employee_app/profile.html')

# def public_biodata_form(request):
#     return render(request, 'employee_app/public_biodata_form.html') 

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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
import openpyxl
from openpyxl.styles import Font

from .models import CustomUser, BioDataRequest
from .forms import BioDataForm, ReviewForm, EditForm
from employee_app.permission_defaults import ROLE_PERMISSIONS
from employee_app.utils import has_permission
from django.core.mail import send_mail
from django.conf import settings

def public_biodata_form(request):
    if request.method == 'POST':
        form = BioDataForm(request.POST, request.FILES)
        if form.is_valid():
            work_exp = []
            employers = request.POST.getlist('prev_employer[]')
            designations = request.POST.getlist('prev_designation[]')
            durations = request.POST.getlist('prev_duration[]')
            emails = request.POST.getlist('prev_email[]')
            cert_files = request.FILES.getlist('work_experience_cert[]')

            for i in range(len(employers)):
                if employers[i].strip():
                    exp = {
                        'employer': employers[i],
                        'designation': designations[i],
                        'duration': durations[i],
                        'email': emails[i],
                    }

                    if i < len(cert_files) and cert_files[i]:
                        cert_file = cert_files[i]
                        from django.core.files.storage import default_storage
                        path = default_storage.save(
                            f'biodata/certs/{cert_file.name}',
                            cert_file
                        )

                        # ✅ ONLY FIX IS HERE
                        exp['certificate_path'] = default_storage.url(path)

                    work_exp.append(exp)

            bio = form.save(commit=False)
            bio.work_experience = work_exp
            bio.save()

            # Notify admin and super_admin about new submission
            for user in CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True):
                link = reverse('employee_app:review_biodata_detail', args=[bio.pk])
                create_notification(
                    recipient=user,
                    ntype='biodata_new',
                    title='New BioData Submission',
                    message=f"{bio.first_name} {bio.last_name} submitted a new bio data request.",
                    link=request.build_absolute_uri(link)
                )

            messages.success(
                request,
                'Bio data submitted successfully! Awaiting HR review.'
            )
            return redirect('employee_app:public_biodata_form')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BioDataForm()

    return render(
        request,
        'employee_app/public_biodata_form.html',
        {'form': form}
    )


@login_required
def pending_requests(request):
    requests = BioDataRequest.objects.all().order_by('-created_at')
    return render(request, 'employee_app/pending_requests.html', {'requests': requests})

@login_required
def review_biodata_detail(request, pk):
    bio = get_object_or_404(BioDataRequest, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=bio)
        if form.is_valid():
            action = request.POST.get('action')

            bio = form.save(commit=False)

            if action == 'approve':
                # HR details are already saved by form.save()
                bio.status = 'approved'
                bio.approved_by = request.user
                messages.success(request, 'Employee approved and details saved successfully!')

                # Send detailed approval email with HR info
                subject = 'Your Application Has Been Approved!'
                message = f"""
                        Dear {bio.first_name} {bio.last_name},

                        Congratulations! Your bio data submission has been approved.

                        Employee Details:
                        - Employee ID: {bio.employee_id}
                        - Official Email: {bio.official_email}
                        - Designation: {bio.designation}
                        - Department: {bio.department}
                        - Date of Joining: {bio.doj.strftime('%d %B %Y') if bio.doj else 'TBD'}
                        - Work Mode: {bio.work_mode or 'Not specified'}

                        Please check your official email for further instructions.

                        Best regards,
                        HR Team - STACKLY
                        """
                send_mail(subject, message.strip(), settings.DEFAULT_FROM_EMAIL, [bio.personal_email])

                # === NOTIFICATION: BioData approved → notify admin & super_admin ===
                for notifier in CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True):
                    link = reverse('employee_app:view_biodata', args=[bio.pk])
                    create_notification(
                        recipient=notifier,
                        ntype='biodata_approved',
                        title='BioData Approved',
                        message=f"{bio.first_name} {bio.last_name}'s request was approved by {request.user.get_full_name() or request.user.email}.",
                        link=request.build_absolute_uri(link)
                    )

            elif action == 'reject':
                bio.status = 'rejected'
                messages.success(request, 'Application rejected successfully.')
                send_mail(
                    'Application Rejected',
                    f'Reason: {bio.reject_reason}',
                    settings.DEFAULT_FROM_EMAIL,
                    [bio.personal_email]
                )

                # === NOTIFICATION: BioData rejected → notify admin & super_admin ===
                for notifier in CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True):
                    link = reverse('employee_app:review_biodata_detail', args=[bio.pk])
                    create_notification(
                        recipient=notifier,
                        ntype='biodata_rejected',
                        title='BioData Rejected',
                        message=f"{bio.first_name} {bio.last_name}'s request was rejected by {request.user.get_full_name() or request.user.email}. Reason: {bio.reject_reason}",
                        link=request.build_absolute_uri(link)
                    )

            bio.save()
            return redirect('employee_app:pending_requests')

    else:
        form = ReviewForm(instance=bio)

    return render(request, 'employee_app/review_biodata_detail.html', {'bio': bio, 'form': form})


from django.db.models import Q

@login_required
def biodata_list(request):
    employees = BioDataRequest.objects.filter(status='approved').order_by('-doj')

    # Get filter parameters from URL
    search = request.GET.get('search', '').strip()
    department = request.GET.get('department', '').strip()

    # Apply search filter (name, email, employee_id)
    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(middle_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(employee_id__icontains=search) |
            Q(official_email__icontains=search) |
            Q(personal_email__icontains=search)
        )

    # Apply department filter
    if department:
        employees = employees.filter(department=department)

    context = {
        'employees': employees,
        'current_search': search,           # to keep input filled
        'current_department': department,   # to keep dropdown selected
    }
    return render(request, 'employee_app/biodata.html', context)

@login_required
def view_biodata(request, pk):
    bio = get_object_or_404(BioDataRequest, pk=pk, status='approved')
    return render(request, 'employee_app/view_biodata.html', {'bio': bio})

@login_required
def edit_biodata(request, pk):
    bio = get_object_or_404(BioDataRequest, pk=pk, status='approved')

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=bio)
        if form.is_valid():
            form.save()
            
            # === NOTIFICATION: BioData edited → notify admin & super_admin ===
            for notifier in CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True):
                link = reverse('employee_app:view_biodata', args=[bio.pk])
                create_notification(
                    recipient=notifier,
                    ntype='biodata_updated',
                    title='Employee BioData Updated',
                    message=f"BioData of {bio.first_name} {bio.last_name} (ID: {bio.employee_id or 'N/A'}) was updated by {request.user.get_full_name() or request.user.email}.",
                    link=request.build_absolute_uri(link)
                )

            messages.success(request, 'Employee bio data updated successfully!')
            return redirect('view_biodata', pk=bio.pk)
    else:
        form = EditForm(instance=bio)

    return render(request, 'employee_app/edit_biodata.html', {'form': form, 'bio': bio})


@login_required
def delete_biodata(request, pk):
    if not has_permission(request.user, 'biodata', 'delete'):
        return HttpResponse('Access Denied', status=403)

    bio = get_object_or_404(BioDataRequest, pk=pk, status='approved')

    if request.method == 'POST':
        deleted_name = f"{bio.first_name} {bio.last_name}"
        deleted_email = bio.personal_email
        bio.delete()

        # === NOTIFICATION: BioData deleted → notify admin & super_admin ===
        for notifier in CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True):
            create_notification(
                recipient=notifier,
                ntype='biodata_deleted',
                title='Employee BioData Deleted',
                message=f"BioData of {deleted_name} ({deleted_email}) was deleted by {request.user.get_full_name() or request.user.email}.",
            )

        messages.success(request, f"BioData of {deleted_name} deleted successfully.")
        return redirect('employee_app:biodata_list')

    # If GET request → show confirmation page (optional but recommended)
    return render(request, 'employee_app/delete_biodata_confirm.html', {'bio': bio})


from datetime import datetime
from openpyxl.styles import Font, Alignment
@login_required
def export_biodata_excel(request):
    if not has_permission(request.user, 'biodata', 'export'):
        return HttpResponse('Access Denied', status=403)

    employees = BioDataRequest.objects.filter(status='approved').order_by('-doj')

    # Apply the same filters as the list view
    search = request.GET.get('search', '').strip()
    department = request.GET.get('department', '').strip()

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(middle_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(employee_id__icontains=search) |
            Q(official_email__icontains=search) |
            Q(personal_email__icontains=search)
        )

    if department:
        employees = employees.filter(department=department)

    # Now build Excel with filtered employees
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Approved Employees"

    columns = [
        'ID', 'First Name', 'Middle Name', 'Last Name', 'Personal Email', 'Contact Number',
        'Employee ID', 'Official Email', 'Designation', 'Department', 'DOJ', 'Work Mode',
        'Experience Type', 'Post Applied For', 'Blood Group',
        'Address', 'Aadhar No', 'PAN No',
        'Bank Name', 'Branch', 'Account No', 'Account Name', 'IFSC',
        'Technical Skills', 'Created At'
    ]
    ws.append(columns)

    for col_num, cell in enumerate(ws[1], start=1):
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    for emp in employees:
        address = f"{emp.address_line1 or ''} {emp.address_line2 or ''}, {emp.city or ''}, {emp.state or ''} {emp.postal_code or ''}, {emp.get_country_display() or ''}".strip()
        ws.append([
            emp.id,
            emp.first_name,
            emp.middle_name or '-',
            emp.last_name,
            emp.personal_email,
            emp.contact_number,
            emp.employee_id or '-',
            emp.official_email or '-',
            emp.designation or '-',
            emp.department or '-',
            emp.doj.strftime('%Y-%m-%d') if emp.doj else '-',
            emp.work_mode or '-',
            emp.get_experience_type_display(),
            emp.get_post_applied_for_display() or '-',
            emp.blood_group or '-',
            address or '-',
            emp.aadhar_no or '-',
            emp.pan_no or '-',
            emp.bank_name or '-',
            emp.bank_branch or '-',
            emp.account_number or '-',
            emp.account_name or '-',
            emp.ifsc_code or '-',
            emp.technical_skills,
            emp.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    # Auto width + freeze header (same as before)
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws.column_dimensions[column].width = max_length + 2
    ws.freeze_panes = 'A2'

    today = datetime.now().strftime('%Y-%m-%d')
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="approved_employees_{today}.xlsx"'
    wb.save(response)
    return response



from django.http import JsonResponse

@login_required
@require_POST
def mark_all_read(request):
    request.user.notifications.update(is_read=True)
    return JsonResponse({'status': 'ok'})

@login_required
def notifications_all(request):
    notifs = request.user.notifications.all()
    return render(request, 'employee_app/notifications_all.html', {'notifications': notifs})