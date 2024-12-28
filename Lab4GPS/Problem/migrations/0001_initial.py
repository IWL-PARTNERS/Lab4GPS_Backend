# Generated by Django 5.1.4 on 2024-12-25 10:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_title', models.CharField(help_text='Title or short description of the problem.', max_length=255, verbose_name='Problem Title')),
                ('description', models.TextField(help_text='Detailed explanation of the problem.', verbose_name='Problem Description')),
                ('category', models.CharField(blank=True, help_text='Either a predefined or user-defined category.', max_length=100, null=True, verbose_name='Problem Category')),
                ('urgency', models.CharField(blank=True, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Critical', 'Critical')], max_length=50, null=True, verbose_name='Urgency Level')),
                ('country', models.CharField(blank=True, help_text='The country of the problem location.', max_length=100, null=True, verbose_name='Country')),
                ('city', models.CharField(blank=True, help_text='The city or town of the problem location.', max_length=100, null=True, verbose_name='City/Town')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, help_text='Decimal latitude of the location.', max_digits=9, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, help_text='Decimal longitude of the location.', max_digits=9, null=True, verbose_name='Longitude')),
                ('media_files', models.JSONField(blank=True, help_text='Array of media file references (images, videos, etc.).', null=True, verbose_name='Media Files')),
                ('submitter_photo', models.CharField(blank=True, help_text="Reference or path to the submitter's photo if provided.", max_length=500, null=True, verbose_name='Submitter Photo Path')),
                ('contact_name', models.CharField(max_length=100, verbose_name='Contact Name')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Contact Email')),
                ('contact_phone', models.CharField(max_length=50, verbose_name='Contact Phone Number')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date Created')),
            ],
        ),
    ]