# Generated by Django 4.2 on 2023-05-10 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
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
            name='OutgoingDocs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tracking_no', models.CharField(max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Received', 'Received'), ('Released', 'Released')], default='Pending', max_length=255)),
                ('date_forwarded', models.DateTimeField(blank=True, null=True)),
                ('tracking_details', models.JSONField(blank=True, null=True)),
                ('doc_actions', models.CharField(choices=[('Approved', 'Approved'), ('Disapproved', 'Disapproved'), ('Signed', 'Signed'), ('Endorsed', 'Endorsed'), ('No Action', 'No Action')], default='No Action', max_length=255)),
                ('forwarded_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forwarded_to', to=settings.AUTH_USER_MODEL)),
                ('type_of_document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Outgoing Doc',
                'verbose_name_plural': 'Outgoing Docs',
            },
        ),
    ]
