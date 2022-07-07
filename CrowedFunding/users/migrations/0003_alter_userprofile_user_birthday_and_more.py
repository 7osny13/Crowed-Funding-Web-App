# Generated by Django 4.0.5 on 2022-07-02 20:08

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_birthday',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.BigIntegerField(default=None),
        ),
    ]
