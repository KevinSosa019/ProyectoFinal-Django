# Generated by Django 5.0.4 on 2024-04-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_delete_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_denounced',
            field=models.BooleanField(default=False),
        ),
    ]
