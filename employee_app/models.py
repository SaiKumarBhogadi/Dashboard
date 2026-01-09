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
        ('employee', 'Employee'),
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

    objects = CustomUserManager()

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

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'), 
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    COUNTRY_CHOICES = (
        ('india', 'India'),
        ('usa', 'USA'),
        ('canada', 'Canada'),
        ('uk', 'UK'),
        ('australia', 'Australia'),
        # Add more countries as needed
    )

    POST_APPLIED_FOR_CHOICES = (
        ('junior_developer', 'Junior Developer'),
        ('frontend_developer', 'Frontend Developer'),
        ('full_stack_developer', 'Full Stack Developer'),
        ('qa_engineer', 'QA Engineer'),
        # Add more as needed
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
        ('Prefer not to say', 'Prefer not to say'),
    )

    MARITAL_STATUS_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )

    EXPERIENCE_TYPE_CHOICES = (
        ('fresher', 'Fresher'),
        ('experienced', 'Experienced'),
    )

    # Personal
    user = models.OneToOneField(
        'CustomUser',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='bio_data_request',
        verbose_name="Linked Employee Account"
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    contact_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20, blank=True)
    personal_email = models.EmailField(unique=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, blank=True)
    aadhar_no = models.CharField(max_length=20, blank=True)
    pan_no = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_branch = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    account_name = models.CharField(max_length=255, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES)
    post_applied_for = models.CharField(max_length=50, choices=POST_APPLIED_FOR_CHOICES, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)

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

    # Work Experience (dynamic + certificate)
    work_experience = models.JSONField(default=list, blank=True)  # stores list of dicts from prev_employer[], etc.

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
        return f"{self.first_name} {self.last_name} - {self.personal_email}"

    class Meta:
        ordering = ['-created_at']

    def get_status_class(self):
        return {'pending': 'pending', 'approved': 'completed', 'rejected': 'danger'}[self.status]
    

class Notification(models.Model):
    recipient = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=50)  # e.g., 'biodata_new', 'biodata_approved'
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True, null=True)  # optional URL
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f"{self.title} → {self.recipient.email if self.recipient else 'Deleted'}"
    

from django.db.models.signals import post_save
from django.dispatch import receiver

# Flag to prevent infinite recursion
_syncing = False

@receiver(post_save, sender=CustomUser)
def sync_user_to_biodata(sender, instance, **kwargs):
    global _syncing
    if _syncing:
        return  # Prevent loop
    if hasattr(instance, 'bio_data_request'):
        _syncing = True
        try:
            biodata = instance.bio_data_request
            biodata.department = instance.department
            biodata.contact_number = instance.phone or biodata.contact_number
            biodata.save(update_fields=['department', 'contact_number'])
        finally:
            _syncing = False

@receiver(post_save, sender=BioDataRequest)
def sync_biodata_to_user(sender, instance, **kwargs):
    global _syncing
    if _syncing:
        return
    if instance.user:
        _syncing = True
        try:
            user = instance.user
            user.department = instance.department
            user.phone = instance.contact_number or user.phone
            user.save(update_fields=['department', 'phone'])
        finally:
            _syncing = False