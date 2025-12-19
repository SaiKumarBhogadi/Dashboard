from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(_('email address'), unique=True)

    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin (HR)'),
        ('scrum_master', 'Scrum Master'),
        ('trainer', 'Trainer'),
    )

    DEPARTMENT_CHOICES = (
        ('software-dev', 'Software Development'),
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('operations', 'Operations'),
        ('training', 'Training & Development'),
        ('', 'Not Specified'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    permissions = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # 🔥 THIS LINE IS REQUIRED

    def __str__(self):
        return self.email


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BioDataRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    # Personal
    full_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    contact_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20, blank=True)
    personal_email = models.EmailField(unique=True)  # Unique as requested
    address = models.TextField(blank=True)
    aadhar_no = models.CharField(max_length=20, blank=True)
    pan_no = models.CharField(max_length=20, blank=True)
    bank_details = models.TextField(blank=True)
    experience_type = models.CharField(max_length=20)  # fresher/experienced

    # Files
    photo = models.ImageField(upload_to='biodata/photos/')
    resume = models.FileField(upload_to='biodata/resumes/')
    aadhar_card = models.FileField(upload_to='biodata/docs/', null=True, blank=True)
    pan_card = models.FileField(upload_to='biodata/docs/', null=True, blank=True)

    # Education
    ssc_school = models.CharField(max_length=255)
    ssc_year = models.PositiveIntegerField()
    ssc_grade = models.CharField(max_length=20)
    ssc_marksheet = models.FileField(upload_to='biodata/docs/')

    sslc_school = models.CharField(max_length=255)
    sslc_year = models.PositiveIntegerField()
    sslc_grade = models.CharField(max_length=20)
    sslc_marksheet = models.FileField(upload_to='biodata/docs/')

    ug_degree = models.CharField(max_length=255)
    ug_institution = models.CharField(max_length=255)
    ug_year = models.PositiveIntegerField()
    ug_documents = models.FileField(upload_to='biodata/docs/')

    pg_degree = models.CharField(max_length=255, blank=True)
    pg_institution = models.CharField(max_length=255, blank=True)
    pg_year = models.PositiveIntegerField(null=True, blank=True)
    pg_documents = models.FileField(upload_to='biodata/docs/', null=True, blank=True)

    cert_course = models.CharField(max_length=255, blank=True)
    cert_institution = models.CharField(max_length=255, blank=True)
    cert_year = models.PositiveIntegerField(null=True, blank=True)
    cert_document = models.FileField(upload_to='biodata/docs/', null=True, blank=True)

    work_experience = models.JSONField(default=list, blank=True)

    technical_skills = models.TextField()
    soft_skills = models.TextField(blank=True)
    reference_name = models.CharField(max_length=255, blank=True)
    reference_contact = models.CharField(max_length=20, blank=True)

    # HR Editable Fields
    employee_id = models.CharField(max_length=30, blank=True)
    official_email = models.EmailField(blank=True)
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    doj = models.DateField(null=True, blank=True)
    work_mode = models.CharField(max_length=20, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reject_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.personal_email}"

    class Meta:
        ordering = ['-created_at']

    def get_status_class(self):
        return {'pending': 'pending', 'approved': 'completed', 'rejected': 'danger'}[self.status]