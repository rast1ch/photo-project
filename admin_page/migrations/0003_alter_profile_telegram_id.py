# Generated by Django 3.2.5 on 2021-07-21 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0002_alter_profile_ref_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telegram_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]