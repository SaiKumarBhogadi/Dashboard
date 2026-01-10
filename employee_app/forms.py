from django import forms
from .models import BioDataRequest

class BioDataForm(forms.ModelForm):
    class Meta:
        model = BioDataRequest
        fields = [
            'first_name', 'middle_name', 'last_name', 'dob', 'gender', 'marital_status',
            'contact_number', 'emergency_contact', 'personal_email',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'aadhar_no', 'pan_no',
            'bank_name', 'bank_branch', 'account_number', 'account_name', 'ifsc_code',
            'experience_type', 'post_applied_for', 'blood_group',
            'photo', 'resume', 'aadhar_card', 'pan_card',
            'ssc_school', 'ssc_year', 'ssc_grade', 'ssc_marksheet',
            'sslc_school', 'sslc_year', 'sslc_grade', 'sslc_marksheet',
            'ug_degree', 'ug_institution', 'ug_year', 'ug_documents',
            'pg_degree', 'pg_institution', 'pg_year', 'pg_documents',
            'cert_course', 'cert_institution', 'cert_year', 'cert_document',
            'technical_skills', 'soft_skills',
            'reference_name', 'reference_contact',
        ]

        widgets = {
            # Date fields
            'dob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select date of birth'}),

            # Dropdowns (placeholders added via first blank option in template or model)
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'experience_type': forms.Select(attrs={'class': 'form-control'}),
            'post_applied_for': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),

            # Textareas with placeholders
            'technical_skills': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'e.g., Python, React, Django, AWS, SQL, JavaScript'
            }),
            'soft_skills': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'e.g., Communication, Teamwork, Leadership, Problem Solving'
            }),

            # Text inputs with meaningful placeholders
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your middle name (optional)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9876543210'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9876543210 (optional)'}),
            'personal_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g., yourname@example.com'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House No, Street name'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment, Landmark (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mumbai'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Maharashtra'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 400001'}),
            'aadhar_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1234 5678 9012'}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ABCDE1234F'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., State Bank of India'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Andheri West Branch'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 123456789012'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., John Doe'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., SBIN0001234'}),
            'ssc_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., St. Mary\'s School, Mumbai'}),
            'ssc_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2018'}),
            'ssc_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 92% or A1'}),
            'sslc_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Maharashtra Board School, Pune'}),
            'sslc_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2020'}),
            'sslc_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 88% or A'}),
            'ug_degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., B.Tech in Computer Science'}),
            'ug_institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., IIT Bombay'}),
            'ug_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2024'}),
            'pg_degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., M.Tech in AI (optional)'}),
            'pg_institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., IIT Delhi (optional)'}),
            'pg_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2026 (optional)'}),
            'cert_course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AWS Certified Solutions Architect (optional)'}),
            'cert_institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Amazon Web Services (optional)'}),
            'cert_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2025 (optional)'}),
            'reference_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mr. Rajesh Kumar (optional)'}),
            'reference_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9876543210 (optional)'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Required fields custom validation
        required_fields = [
            'first_name', 'last_name', 'contact_number', 'personal_email',
            'experience_type', 'technical_skills',
            'ssc_school', 'ssc_year', 'ssc_grade',
            'sslc_school', 'sslc_year', 'sslc_grade',
            'ug_degree', 'ug_institution', 'ug_year',
        ]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required.')

        # File size & type validation
        max_size = 5 * 1024 * 1024  # 5MB
        allowed_types = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
        file_fields = [
            'photo', 'resume', 'aadhar_card', 'pan_card',
            'ssc_marksheet', 'sslc_marksheet', 'ug_documents', 'pg_documents',
            'cert_document',
        ]
        for field in file_fields:
            file = cleaned_data.get(field)
            if file:
                if file.size > max_size:
                    self.add_error(field, 'File too large (max 5MB)')
                if file.content_type not in allowed_types:
                    self.add_error(field, 'Only PDF, JPG, JPEG, PNG allowed')

        return cleaned_data

    def clean_personal_email(self):
        email = self.cleaned_data['personal_email']
        if BioDataRequest.objects.filter(personal_email=email).exists():
            raise forms.ValidationError("This email has already been used for a submission.")
        return email


from django.core.exceptions import ValidationError
from .models import BioDataRequest, CustomUser
from django import forms
from django.core.exceptions import ValidationError
from .models import BioDataRequest, CustomUser

class ReviewForm(forms.ModelForm):
    create_account = forms.BooleanField(
        required=False,
        initial=True,
        label="Create Employee Account?",
        help_text="If checked, a login account will be created."
    )

    class Meta:
        model = BioDataRequest
        fields = ['employee_id', 'official_email', 'designation', 'department', 'doj', 'work_mode', 'reject_reason', 'create_account']
        widgets = {
            'reject_reason': forms.Textarea(attrs={'rows': 4}),
            'doj': forms.DateInput(attrs={'type': 'date'}),
            'employee_id': forms.TextInput(attrs={'placeholder': 'e.g., EMP-2025-156'}),
            'official_email': forms.EmailInput(attrs={'placeholder': 'employee@stackly.com'}),
            'designation': forms.Select(choices=[('', 'Select'),('Junior Developer', 'Junior Developer'),('Frontend Developer', 'Frontend Developer'),('Backend Developer', 'Backend Developer'),('Full Stack Developer', 'Full Stack Developer'),('QA Engineer', 'QA Engineer'),]),

           'department': forms.Select(choices=CustomUser.DEPARTMENT_CHOICES),

            'work_mode': forms.Select(choices=[('', 'Select'), ('Remote', 'Remote'), ('Onsite', 'Onsite'), ('Hybrid', 'Hybrid')]),
        }

    def clean_official_email(self):
        email = self.cleaned_data.get('official_email')
        if email:
            # Prevent duplicate in CustomUser
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError("This official email is already used by another employee.")
            # Prevent duplicate in other BioDataRequest
            current_id = self.instance.pk if self.instance else None
            if BioDataRequest.objects.exclude(pk=current_id).filter(official_email=email).exists():
                raise ValidationError("This official email is already assigned to another biodata.")
        return email

    def clean_employee_id(self):
        emp_id = self.cleaned_data.get('employee_id')
        if emp_id:
            current_id = self.instance.pk if self.instance else None
            if BioDataRequest.objects.exclude(pk=current_id).filter(employee_id=emp_id).exists():
                raise ValidationError("This Employee ID is already in use.")
        return emp_id

class BioDataEditForm(forms.ModelForm):
    class Meta:
        model = BioDataRequest
        fields = [
            'first_name', 'middle_name', 'last_name', 'dob', 'gender', 'marital_status',
            'contact_number', 'emergency_contact', 'personal_email',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            'aadhar_no', 'pan_no', 'bank_name', 'bank_branch', 'account_number', 'account_name', 'ifsc_code',
            'experience_type', 'post_applied_for', 'blood_group',
            'ssc_school', 'ssc_year', 'ssc_grade', 'ssc_marksheet',  # SSC
            'sslc_school', 'sslc_year', 'sslc_grade', 'sslc_marksheet',  # SSLC
            'ug_degree', 'ug_institution', 'ug_year', 'ug_documents',  # UG
            'pg_degree', 'pg_institution', 'pg_year', 'pg_documents',  # PG
            'cert_course', 'cert_institution', 'cert_year', 'cert_document',  # Certification
            'technical_skills', 'soft_skills', 'reference_name', 'reference_contact',
            'employee_id', 'official_email', 'designation', 'department', 'doj', 'work_mode',
            'photo', 'resume', 'aadhar_card', 'pan_card',
        ]
        exclude = ['status', 'reject_reason', 'approved_by', 'created_at', 'updated_at', 'user', 'work_experience']  # exclude dynamic JSON
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'doj': forms.DateInput(attrs={'type': 'date'}),
            'department': forms.Select(choices=CustomUser.DEPARTMENT_CHOICES),
            'designation': forms.Select(choices=[('', 'Select'), ('Junior Developer', 'Junior Developer'), ('Frontend Developer', 'Frontend Developer'), ('Backend Developer', 'Backend Developer'), ('Full Stack Developer', 'Full Stack Developer'), ('QA Engineer', 'QA Engineer')]),
            'technical_skills': forms.Textarea(attrs={'rows': 3}),
            'soft_skills': forms.Textarea(attrs={'rows': 3}),
        }

# NEW: Dedicated form for editing users (replaces manual POST handling)
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone', 'department', 'role', 'status']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),  # readonly in edit
            'department': forms.Select(choices=CustomUser.DEPARTMENT_CHOICES),
            'role': forms.Select(choices=CustomUser.ROLE_CHOICES),
            'status': forms.Select(choices=CustomUser.STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True



# For employee self-edit (limited fields)
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = BioDataRequest
        fields = ['contact_number', 'emergency_contact', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }



# employee_app/forms.py

from django import forms
from .models import Batch, Session, Assignment, Submission
# forms.py

from django import forms
from .models import Batch, CustomUser


class BatchCreateForm(forms.ModelForm):
    """
    Form for CREATING new batch - only show currently unassigned employees
    """
    class Meta:
        model = Batch
        fields = ['name', 'start_date', 'end_date', 'description', 'status', 'trainers', 'employees']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'trainers': forms.SelectMultiple(attrs={'class': 'form-control select2-multi'}),
            'employees': forms.SelectMultiple(attrs={'class': 'form-control select2-multi'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Trainers → ONLY people with role='trainer'
        self.fields['trainers'].queryset = CustomUser.objects.filter(
            role='trainer',                    # ← Fixed: only trainers
            is_active=True
        ).order_by('full_name')

        # Employees → only currently unassigned
        unassigned = CustomUser.objects.filter(
            role='employee',
            is_active=True,
            enrolled_batches__isnull=True
        ).select_related('bio_data_request').order_by('full_name')

        choices = [
            (emp.id, f"{emp.full_name} ({getattr(emp.bio_data_request, 'employee_id', 'N/A')} - {emp.email})")
            for emp in unassigned
        ]

        self.fields['employees'].choices = choices
        self.fields['employees'].queryset = unassigned


class BatchUpdateForm(BatchCreateForm):
    """
    Form for UPDATING existing batch - show ALL active employees
    so that already assigned ones can be removed
    """
    class Meta(BatchCreateForm.Meta):
        exclude = ['created_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Trainers → same restriction as create (only 'trainer')
        self.fields['trainers'].queryset = CustomUser.objects.filter(
            role='trainer',
            is_active=True
        ).order_by('full_name')

        # Employees → ALL active (can add or remove)
        all_employees = CustomUser.objects.filter(
            role='employee',
            is_active=True
        ).select_related('bio_data_request').order_by('full_name')

        choices = [
            (emp.id, f"{emp.full_name} ({getattr(emp.bio_data_request, 'employee_id', 'N/A')} - {emp.email})")
            for emp in all_employees
        ]

        self.fields['employees'].choices = choices
        self.fields['employees'].queryset = all_employees

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Session

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Session, Batch, CustomUser

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'batch', 'trainer', 'date_time', 'duration_hours', 'agenda', 'meeting_link', 'status', 'notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'agenda': forms.Textarea(attrs={'rows': 5, 'placeholder': 'List topics, exercises, key points...'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Prerequisites, special instructions, recording info...'}),
            'meeting_link': forms.URLInput(attrs={'placeholder': 'https://zoom.us/j/... or https://meet.google.com/...'}),
        }
        labels = {
            'title': 'Session Title *',
            'batch': 'Batch *',
            'trainer': 'Lead Trainer',
            'date_time': 'Date & Time *',
            'duration_hours': 'Duration (hours)',
            'agenda': 'Agenda / Topics',
            'meeting_link': 'Meeting Link',
            'status': 'Status',
            'notes': 'Additional Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: You can keep default queryset for trainer (all possible trainers)
        # We will enforce correct trainer in clean() below
        self.fields['trainer'].queryset = CustomUser.objects.filter(
            role__in=['trainer', 'admin', 'super_admin'],
            is_active=True
        ).order_by('full_name')

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if not date_time:
            raise ValidationError("Date and time are required.")
        if date_time < timezone.now():
            raise ValidationError("Cannot schedule a session in the past.")
        return date_time

    def clean_duration_hours(self):
        duration = self.cleaned_data.get('duration_hours')
        if duration is not None:
            if duration < 0.5:
                raise ValidationError("Duration must be at least 30 minutes.")
            if duration > 8:
                raise ValidationError("Duration cannot exceed 8 hours (please split into multiple sessions).")
        return duration

    def clean_meeting_link(self):
        link = self.cleaned_data.get('meeting_link')
        if link and not link.startswith(('http://', 'https://')):
            raise ValidationError("Please enter a valid URL (starting with http:// or https://).")
        return link

    def clean(self):
        cleaned_data = super().clean()
        batch = cleaned_data.get('batch')
        trainer = cleaned_data.get('trainer')

        # Enforce: trainer must be one of the batch's assigned trainers (if both selected)
        if batch and trainer:
            if trainer not in batch.trainers.all():
                self.add_error('trainer', ValidationError(
                    f"Selected trainer ({trainer.full_name or trainer.email}) is not assigned to this batch ({batch.name}). "
                    "Please choose a trainer from the batch's assigned trainers list."
                ))

        return cleaned_data


# Edit form inherits the same validations
class SessionEditForm(SessionForm):
    class Meta(SessionForm.Meta):
        exclude = ['created_by', 'batch']  # Don't allow changing batch after creation

    def clean(self):
        cleaned_data = super().clean()
        trainer = cleaned_data.get('trainer')

        # For edit: use the existing session's batch to validate trainer
        if self.instance and self.instance.pk:
            batch = self.instance.batch
            if trainer and trainer not in batch.trainers.all():
                self.add_error('trainer', ValidationError(
                    f"Selected trainer ({trainer.full_name or trainer.email}) is not assigned to this batch ({batch.name})."
                ))

        return cleaned_data





# Assignment Forms
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'batch', 'session', 'due_date', 'max_score', 'description', 'rubric', 'submission_format', 'status', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 6}),
            'rubric': forms.Textarea(attrs={'rows': 4}),
            'submission_format': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class AssignmentEditForm(AssignmentForm):
    class Meta(AssignmentForm.Meta):
        exclude = ['created_by', 'batch']  # Usually don't change batch


# Submission Form (for employees to submit)
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.zip,.pdf,.py,.docx,.jpg,.png'}),
        }