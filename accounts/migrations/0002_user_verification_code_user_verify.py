# Generated by Django 5.1.2 on 2024-11-02 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Təsdiq Kodu'),
        ),
        migrations.AddField(
            model_name='user',
            name='verify',
            field=models.BooleanField(default=False, verbose_name='Təsdiqlənib'),
        ),
    ]