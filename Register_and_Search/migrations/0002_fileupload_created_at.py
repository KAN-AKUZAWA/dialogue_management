# Generated by Django 4.2.3 on 2023-07-22 08:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Register_and_Search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
