# Generated by Django 5.0.7 on 2024-09-13 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_content_comment_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]