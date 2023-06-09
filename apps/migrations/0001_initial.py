# Generated by Django 4.2 on 2023-05-21 15:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('employee_no', models.CharField(max_length=255, unique=True)),
                ('profile_picture', models.ImageField(default='default.png', upload_to='profile_picture')),
                ('contact', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^\\d{11}$', 'Phone number must be 11 digits long.')])),
                ('is_employee', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(default='RECEIVED', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('office', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Tracking',
                'verbose_name_plural': 'Trackings',
            },
        ),
        migrations.CreateModel(
            name='OutgoingDocs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tracking_no', models.CharField(max_length=255, unique=True)),
                ('title_docs', models.CharField(max_length=255, verbose_name='Title of the Document')),
                ('document', models.FileField(upload_to='documents')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Forwarded', 'Forwarded'), ('Denied', 'Denied')], default='Pending', max_length=255)),
                ('date_forwarded', models.DateTimeField(auto_now_add=True)),
                ('tracking_details', models.JSONField(blank=True, null=True)),
                ('doc_actions', models.CharField(choices=[('Approved', 'Approved'), ('Disapproved', 'Disapproved'), ('Signed', 'Signed'), ('Endorsed', 'Endorsed'), ('No Action', 'No Action')], default='No Action', max_length=255, verbose_name='Document Actions:')),
                ('forwarded_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.department', verbose_name='Forwarded To:')),
                ('type_of_document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Outgoing Document',
                'verbose_name_plural': 'Outgoing Documents',
            },
        ),
        migrations.CreateModel(
            name='IncomingDocs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tracking_no', models.CharField(max_length=255, unique=True)),
                ('title_docs', models.CharField(max_length=255, verbose_name='Title of the Document')),
                ('document', models.FileField(upload_to='documents')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Forwarded', 'Forwarded'), ('Denied', 'Denied')], default='Pending', max_length=255)),
                ('date_forwarded', models.DateTimeField(auto_now_add=True)),
                ('tracking_details', models.JSONField(blank=True, null=True)),
                ('doc_actions', models.CharField(choices=[('Approved', 'Approved'), ('Disapproved', 'Disapproved'), ('Signed', 'Signed'), ('Endorsed', 'Endorsed'), ('No Action', 'No Action')], default='No Action', max_length=255)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_by', to='apps.department')),
                ('type_of_document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Incoming Document',
                'verbose_name_plural': 'Incoming Documents',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
