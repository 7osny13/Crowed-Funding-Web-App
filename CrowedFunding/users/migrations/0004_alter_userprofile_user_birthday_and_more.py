# Generated by Django 4.0.5 on 2022-07-04 17:35

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_userprofile_user_birthday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
