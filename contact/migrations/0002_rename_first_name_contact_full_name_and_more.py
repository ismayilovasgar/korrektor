# Generated by Django 5.1.2 on 2024-11-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='title',
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=60),
        ),
    ]
