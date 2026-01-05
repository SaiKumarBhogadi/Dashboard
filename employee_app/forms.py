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

# For HR Review (Approve/Reject)
class ReviewForm(forms.ModelForm):
    class Meta:
        model = BioDataRequest
        fields = ['employee_id', 'official_email', 'designation', 'department', 'doj', 'work_mode', 'reject_reason']
        widgets = {
            'reject_reason': forms.Textarea(attrs={'rows': 4}),
            'doj': forms.DateInput(attrs={'type': 'date'}),
        }


# For Editing Approved Employee
class EditForm(forms.ModelForm):
    class Meta:
        model = BioDataRequest
        fields = '__all__'
        exclude = ['status', 'reject_reason', 'approved_by', 'created_at', 'updated_at']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'doj': forms.DateInput(attrs={'type': 'date'}),
            'technical_skills': forms.Textarea(attrs={'rows': 3}),
            'soft_skills': forms.Textarea(attrs={'rows': 3}),
        }