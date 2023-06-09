from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
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


#model for department
class Department(models.Model):
    department = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department
    
#model for user
class User(AbstractUser):
    USERNAME_FIELD = 'employee_no'# changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS
    username = models.CharField(max_length=255, null=True, blank=True)
    employee_no = models.CharField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to="profile_picture", default='default.png')
    phone_regex = RegexValidator(r'^\d{11}$', 'Phone number must be 11 digits long.')
    contact = models.CharField(max_length=11, validators=[phone_regex])
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.employee_no
    

#model for document type
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category 

#model for outgoing documents
class OutgoingDocs(models.Model):
    docs_status = (
        ('Pending', 'Pending'),
        ('Forwarded', 'Forwarded'),
        ('Denied', 'Denied'),
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
    title_docs = models.CharField(max_length=255, verbose_name="Title of the Document")
    type_of_document = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    document = models.FileField(upload_to="documents")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="Pending", choices=docs_status)
    forwarded_to = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True,verbose_name="Forwarded To:")
    date_forwarded = models.DateTimeField(auto_now_add=True)
    tracking_details = models.JSONField(null=True, blank=True)
    doc_actions = models.CharField(max_length=255, default="No Action", choices=docs_actions, verbose_name="Document Actions:")

    class Meta:
        verbose_name = 'Outgoing Document'
        verbose_name_plural = 'Outgoing Documents'

    def __str__(self):
        return self.tracking_no

#model for incoming documents
class IncomingDocs(models.Model):
    choices_status = (
        ('Pending', 'Pending'),
        ('Forwarded', 'Forwarded'),
        ('Denied', 'Denied'),
    )
    actions = (
        ("Approved", "Approved"),
        ("Disapproved", "Disapproved"),
        ("Signed", "Signed"),
        ("Endorsed", "Endorsed"),
        ("No Action", "No Action"),    
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_no = models.CharField(max_length=255, unique=True)
    title_docs = models.CharField(max_length=255, verbose_name="Title of the Document")
    type_of_document = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    document = models.FileField(upload_to="documents")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="Pending", choices=choices_status)
    receiver = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, related_name="received_by")
    date_forwarded = models.DateTimeField(auto_now_add=True)
    tracking_details = models.JSONField(null=True, blank=True)
    doc_actions = models.CharField(max_length=255, default="No Action", choices=actions)

    class Meta:
        verbose_name = 'Incoming Document'
        verbose_name_plural = 'Incoming Documents'

    def __str__(self):
        return self.receiver

    

class Tracking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=255, default="RECEIVED")
    created = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    office = models.CharField(max_length=255)
    docs = models.ForeignKey(OutgoingDocs, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Tracking'
        verbose_name_plural = 'Trackings'


class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="created_by_user")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255)


    def __str__(self):
        return self.message