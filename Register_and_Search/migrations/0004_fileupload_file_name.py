# Generated by Django 4.2.3 on 2023-07-22 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Register_and_Search', '0003_rename_uploaded_date_dialogue_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]