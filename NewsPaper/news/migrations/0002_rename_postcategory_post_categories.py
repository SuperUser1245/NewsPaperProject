# Generated by Django 4.2.6 on 2023-10-29 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='postCategory',
            new_name='categories',
        ),
    ]
