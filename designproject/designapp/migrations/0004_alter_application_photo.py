# Generated by Django 5.1.3 on 2024-11-10 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designapp', '0003_application_design_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='photo',
            field=models.ImageField(null=True, upload_to='media/photos/'),
        ),
    ]
