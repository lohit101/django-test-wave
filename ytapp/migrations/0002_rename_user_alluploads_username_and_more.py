# Generated by Django 5.0.7 on 2024-07-21 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ytapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alluploads',
            old_name='user',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='lastupload',
            old_name='user',
            new_name='username',
        ),
    ]
