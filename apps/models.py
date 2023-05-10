from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import uuid
# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, employee_no, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not employee_no:
            raise ValueError('The Employee No must be set')
        email = self.normalize_email(employee_no)
        user = self.model(employee_no=employee_no, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, employee_no, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(employee_no, password, **extra_fields)


class User(AbstractUser):

    USERNAME_FIELD = 'employee_no'# changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS
    username = models.CharField(max_length=255, null=True, blank=True)
    employee_no = models.CharField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to="profile_picture", default='default.png')
    contact = models.CharField(max_length=13)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    # department = models.OneToOneField("Department", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.department

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category 


class OutgoingDocs(models.Model):
    docs_status = (
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Released', 'Released'),
    )
    docs_actions = (
        ("Approved", "Approved"),
        ("Disapproved", "Disapproved"),
        ("Signed", "Signed"),
        ("Endorsed", "Endorsed"),
        ("No Action", "No Action"),    
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_no = models.CharField(max_length=255, unique=True)
    type_of_document = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="Pending", choices=docs_status)
    forwarded_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="forwarded_to")
    date_forwarded = models.DateTimeField(null=True, blank=True)
    tracking_details = models.JSONField(null=True, blank=True)
    doc_actions = models.CharField(max_length=255, default="No Action", choices=docs_actions)

    class Meta:
        verbose_name = 'Outgoing Doc'
        verbose_name_plural = 'Outgoing Docs'

    def __str__(self):
        return self.tracking_no