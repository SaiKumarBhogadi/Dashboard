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




# employee_app/models.py (add these at the end)

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Batch(models.Model):
    name = models.CharField(max_length=200, unique=True)
    batch_code = models.CharField(max_length=50, unique=True, blank=True)  # e.g. PYFS-2026-A
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')],
        default='pending'
    )
    trainers = models.ManyToManyField(
        User,
        related_name='trained_batches',
        limit_choices_to={'role__in': ['trainer', 'admin', 'super_admin']}
    )
    employees = models.ManyToManyField(
        User,
        related_name='enrolled_batches',
        limit_choices_to={'role': 'employee'}
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_batches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def progress_percentage(self):
        total = self.sessions.count()
        if total == 0:
            return 0
        completed = self.sessions.filter(status='completed').count()
        return round((completed / total) * 100, 1)

    def save(self, *args, **kwargs):
        if not self.batch_code:
            # Auto-generate code, e.g. first 4 letters of name + year + sequence
            year = self.start_date.year if self.start_date else timezone.now().year
            prefix = self.name[:4].upper().replace(' ', '')
            last_batch = Batch.objects.filter(batch_code__startswith=prefix).order_by('-batch_code').first()
            seq = 1
            if last_batch and '-' in last_batch.batch_code:
                try:
                    seq = int(last_batch.batch_code.split('-')[-1]) + 1
                except:
                    pass
            self.batch_code = f"{prefix}-{year}-{seq:02d}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date']


class Session(models.Model):
    title = models.CharField(max_length=200)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sessions')
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_sessions')
    date_time = models.DateTimeField()
    duration_hours = models.FloatField(default=2.0, validators=[MinValueValidator(0.5)])
    agenda = models.TextField(blank=True)  # renamed from topic_agenda
    meeting_link = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')],
        default='pending'
    )
    notes = models.TextField(blank=True)
    attendance_taken = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.batch.name}"

    class Meta:
        ordering = ['date_time']
    
    @property
    def attendance_percentage(self):
        total = self.batch.employees.count()
        if total == 0 or not self.attendance_taken:
            return 0
        present = self.attendance_records.filter(status='present').count()
        return round((present / total) * 100, 1)


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='assignments')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    due_date = models.DateField()
    max_score = models.PositiveIntegerField(default=100)
    description = models.TextField()
    rubric = models.TextField(blank=True)
    submission_format = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('graded', 'Graded')],
        default='pending'
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    @property
    def total_submissions(self):
        return self.submissions.count()

    @property
    def average_score(self):
        scores = [s.score for s in self.submissions.filter(score__isnull=False)]
        if not scores:
            return 0
        return round(sum(scores) / len(scores), 1)

    class Meta:
        ordering = ['due_date']


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employee'})
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='graded_submissions')
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('assignment', 'employee')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.employee} - {self.assignment}"

    @property
    def is_late(self):
        return self.submitted_at.date() > self.assignment.due_date


class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendance_records')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employee'})
    status = models.CharField(
        max_length=10,
        choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('excused', 'Excused')],
        default='absent'
    )
    notes = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='attendance_marked')
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'employee')
        ordering = ['-marked_at']

    def __str__(self):
        return f"{self.employee} - {self.session}"


class Material(models.Model):
    # Generic relation (can attach to Session or Assignment)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    file = models.FileField(upload_to='training_materials/')
    uploaded_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Material for {self.content_object}"

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]